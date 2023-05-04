from database import Database
from models import User, Driver, Order, Vehicle
from flask import Flask, render_template, jsonify
from flask_swagger import swagger
from flask_cors import CORS
from webargs.flaskparser import use_args
from webargs import fields
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

db = Database()
db.migrate()


@app.get('/')
def index():
    return render_template("index.html")


@app.post('/signup')
@use_args({
    'first_name': fields.Str(required=True, error_messages={'required': 'The first_name field is required'}),
    'last_name': fields.Str(required=True, error_messages={'required': 'The last_name field is required'}),
    'email': fields.Email(required=True, error_messages={'required': 'The email field is required'}),
    'password': fields.Str(required=True, error_messages={'required': 'The password field is required'}),
    'password_confirm': fields.Str(required=True, error_messages={'required': 'The password confirmation field is required'})
}, location='json')
def signup(data):
    """
    Create a new user
    ---
    parameters:
    -   in: body
        name: data
        required:
            - email
            - first_name
            - last_name
            - password
            - password_confirm
        properties:
            email:
                type: string
                description: This is the user's email address
            first_name:
                type: string
                description: This is the user's first name
            last_name:
                type: string
                description: This is the user's last name
            password:
                type: string
                description: This is the user's password
            password_confirm:
                type: string
                description: This is the user's password confirmation
    responses:
        201:
            description: User registered successfully.
        400:
            description: 
                - The passwords do not match.
                - User with email already exist.
    """
    if data['password'] != data['password_confirm']:
        return jsonify({'message': 'The passwords do not match.'}), 400

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    user.set_password(data['password'])
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User with email already exist.'}), 400

    return jsonify({'message': f'User registered successfully.'}), 201


@app.post('/login')
@use_args({
    'email': fields.Email(required=True),
    'password': fields.Str(required=True),
}, location='json')
def signin(data):
    """
    Login a user by generating auth token
    ---
    parameters:
    -   in: body
        name: data
        required:
            - email
            - password
        properties:
            email:
                type: string
                description: This is the user's email address
            password:
                type: string
                description: This is the user's password
    responses:
        201:
            description: User logged in successfully.
        400:
            description: Invalid login credentials.
        500:
            description: Error occured.
    """
    user = (
        db.session
        .query(User)
        .filter((User.email == data['email']))
        .first()
    )
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid login credentials.'}), 400

    try:
        auth_token = user.generate_auth_token(user.id)
    except Exception:
        return jsonify({'message': 'Error occured.'}), 500

    return jsonify({
        'message': 'User logged in successfully.',
        'data': {'token': auth_token}
    }), 200

@app.route('/orders', methods=['POST'])
@use_args({
    'email': fields.Email(required=True),
    'password': fields.Str(required=True),
}, location='json')
def create_order():
    # Get data from the client-side request
    data = request.get_json()

    # Extract the relevant data from the request
    pickup_location = data['pickup_location']
    destination = data['destination']
    comfortability = data['comfortability']
    pickup_datetime = data['pickup_datetime']
    user_email = data['name']
    amount = data['amount']

    # Check if the user exists in the database
    user = User.query.filter_by(email=user_email).first()
    if user:
        user_id = user.id
    else:
        return jsonify({'message': 'User not found'}), 404

    # Get a list of all available vehicles that match the user's requested comfortability
    comfortable_vehicles = Vehicle.query.filter_by(comfortability=comfortability).all()

    if not comfortable_vehicles:
        return jsonify({'message': 'No available vehicles found for the requested comfortability'}), 404

    # Create a list of dictionaries containing information about each available vehicle
    available_vehicles = []
    for vehicle in comfortable_vehicles:
        vehicle_data = {}
        vehicle_data['id'] = vehicle.id
        vehicle_data['make'] = vehicle.make
        vehicle_data['model'] = vehicle.model
        vehicle_data['license_plate'] = vehicle.license_plate
        vehicle_data['driver_id'] = vehicle.driver_id

        available_vehicles.append(vehicle_data)

    # Return the list of available vehicles to the client for them to choose from
    return jsonify({'available_vehicles': available_vehicles}), 200

@app.route('/orders/<int:vehicle_id>', methods=['POST'])
def create_order_with_vehicle(vehicle_id):
    # Get data from the client-side request
    data = request.get_json()

    # Extract the relevant data from the request
    
    pickup_location = data['pickup_location']
    destination = data['destination']
    comfortability = data['comfortability']
    pickup_datetime = data['pickup_datetime']
    user_email = data['name']
    amount = data['amount']



    # Check if the user exists in the database
    user = User.query.filter_by(email=user_email).first()
    if user:
        user_id = user.id
    else:
        return jsonify({'message': 'User not found'}), 404

    # Check if the selected vehicle exists and is available
    selected_vehicle = Vehicle.query.filter_by(id=vehicle_id, comfortability=comfortability).first()
    if not selected_vehicle:
        return jsonify({'message': 'Vehicle not found or not available for the requested comfortability'}), 404


    # Register the order in the database
    new_order = Order(user_id=user_id, driver_id=selected_vehicle.driver_id, vehicle_id=selected_vehicle.id,amount=amount, pickup_location=pickup_location, pickup_datetime=pickup_datetime, destination=destination, comfortability=comfortability)
    db.session.add(new_order)
    db.session.commit() 


@app.route('/bookings/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    # Query the database for the booking with the given ID
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Delete the booking from the database
    db.session.delete(order)
    db.session.commit()

    # Return a success message to the client
    return jsonify({'message': 'Order cancelled successfully'}), 200



@app.get('/spec')
def spec():
    swag = swagger(app)
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'Glidee App API'
    return jsonify(swag)


@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    messages = []
    errors = err.data.get('messages', {}).get('json', {})
    for key in errors.keys():
        messages += errors[key]
    return jsonify({'errors': messages, 'message': 'Some required fields are missing.'}), 400


if __name__ == "__main__":
    app.run(debug=True)
