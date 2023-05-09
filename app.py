from models import User, Driver, Order, Vehicle, db
from flask import Flask, render_template, jsonify
from flask_swagger import swagger
from flask_login import current_user
from webargs import fields, validate
from webargs.flaskparser import use_args
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from send_token import Token


app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

token = Token()
new_token = token.confirm_token()

# home route


@app.get('/')
def index():
    db.create_all()
    return render_template("index.html")

# signup route for new users


@app.route('/signup', methods=["GET", "POST"])
@use_args({
    'first_name': fields.Str(required=True, error_messages={'required': 'The first_name field is required'}),
    'last_name': fields.Str(required=True, error_messages={'required': 'The last_name field is required'}),
    'email': fields.Email(required=True, error_messages={'required': 'The email field is required'}),
    'password': fields.Str(required=True, error_messages={'required': 'The password field is required'}),
    'password_confirm': fields.Str(required=True, error_messages={'required': 'The password confirmation field is required'})
}, location='json')
def signup(data):

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

# login route


@app.route('/login', methods=["GET", "POST"])
@use_args({
    'email': fields.Email(required=True),
    'password': fields.Str(required=True),
}, location='json')
def signin(data):

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


# Forgot email route
@app.route('/forgot_password/<email>', methods=['GET', 'POST'])
@use_args({
    'email': fields.Email(required=True, error_messages={'required': 'The email field is required'})
}, location='json')
def forgot_password(data):

    email = data['email']

    if not email:
        return jsonify({'message': 'Invalid login credentials.'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid email. Please try again.'}), 400

    reset_token = token.send_token(email=email)

    # Here you would send an email to the user containing the reset token
    # I plan to update this code later by using a service like SendGrid or Mailgun to handle this

    return jsonify({'message': 'An email containing instructions to reset your password has been sent.'}), 200

# Reset password route


@app.route('/reset_password', methods=['GET', 'POST'])
@use_args({
    'email': fields.Str(required=True, error_messages={'required': 'The first_name field is required'}),
    'token': fields.Str(required=True, error_messages={'required': 'The last_name field is required'}),
    'new_password': fields.Str(required=True, error_messages={'required': 'The password field is required'}),
    'confirm_password': fields.Str(required=True, error_messages={'required': 'The password confirmation field is required'})
}, location='json')
def reset_password(data):

    email = data['email']
    token = data['token']
    new_password = data['new_password']
    confirm_password = data['confirm_password']

    if not email:
        return jsonify({'message': 'This string can not be empty'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid email. Please try again.'}), 401

    if token != new_token:
        return jsonify({'message': 'Invalid Token. Please try again.'}), 401

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid email. Please try again.'}), 401

    if not new_password:
        return jsonify({'message': 'This string cannot be empty'}), 400

    if new_password != confirm_password:
        return jsonify({'message': 'The passwords you entered do not match. Please make sure that both passwords are the same.'}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password successfully changed.'}), 200

# create order route


@app.route('/orders', methods=["GET", "POST"])
# Get data from the client-side request
@use_args({
    'pickup_location': fields.Str(required=True, error_messages={'required': 'The pickup_location field is required'}),
    'destination': fields.Str(required=True, error_messages={'required': 'The destination field is required'}),
    'comfortability': fields.Str(validate=validate.OneOf(['shared', 'standard', 'Luxury']), required=True, error_messages={'required': 'The comfortability field is required'}),
    'pickup_datetime': fields.DateTime(format='%Y-%m-%dT%H:%M:%S', required=True, error_messages={'required': 'The pickup_datetime field is required'}),
}, location='json')
def create_order(data):

    # Extract the relevant data from the request
    pickup_location = data['pickup_location']
    destination = data['destination']
    comfortability = data['comfortability']
    pickup_datetime = data['pickup_datetime']

    # Get a list of all available vehicles that match the user's requested comfortability
    comfortable_vehicles = Vehicle.query.filter_by(
        comfortability=comfortability).all()

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

# create order with vehicle route.


@app.route('/create_order_with_vehicle', methods=["GET", "POST"])
# Get data from the client-side request
@use_args({
    'pickup_location': fields.Str(required=True, error_messages={'required': 'The pickup_location field is required'}),
    'destination': fields.Str(required=True, error_messages={'required': 'The destination field is required'}),
    'comfortability': fields.Str(validate=validate.OneOf(['shared', 'standard', 'Luxury']), required=True, error_messages={'required': 'The comfortability field is required'}),
    'pickup_datetime': fields.DateTime(format='%Y-%m-%dT%H:%M:%S', required=True, error_messages={'required': 'The pickup_datetime field is required'}),
    'vehicle_id': fields.Str(required=True, error_messages={'required': 'The vehicle_id field is required'})}, location='json')
def create_order_with_vehicle(data):

    current_user_details = current_user()
    user_email = current_user_details.email
    # Extract the relevant data from the request

    pickup_location = data['pickup_location']
    destination = data['destination']
    comfortability = data['comfortability']
    pickup_datetime = data['pickup_datetime']
    vehicle_id = data['vehicle_id']

    # Check if the user exists in the database
    user = User.query.filter_by(email=user_email).first()
    if user:
        user_id = user.id
    else:
        return jsonify({'message': 'User not found'}), 404

    # get vehicle amount in the database
    vehicle_amount = Vehicle.query.filter_by(vehicle_id=vehicle_id).first()
    amount = vehicle_amount.amount

    # Check if the selected vehicle exists and is available
    selected_vehicle = Vehicle.query.filter_by(
        id=vehicle_id, comfortability=comfortability).first()
    if not selected_vehicle:
        return jsonify({'message': 'Vehicle not found or not available for the requested comfortability'}), 404

    # Register the order in the database
    new_order = Order(user_id=user_id, driver_id=selected_vehicle.driver_id, vehicle_id=selected_vehicle.id, amount=amount,
                      pickup_location=pickup_location, pickup_datetime=pickup_datetime, destination=destination, comfortability=comfortability)
    db.session.add(new_order)
    db.session.commit()

# order history route. This is where each user get to see their order history


@app.route('/order_history', methods=["GET", "POST"])

@use_args({
    'user_id': fields.Int(required=True, validate=validate.Range(min=1), error_messages={'required': 'The user_id field is required'})
}, location='query')

def get_user_orders(args):
    user_id = args['user_id']

    # Retrieve all orders of the user from the database
    orders = Order.query.filter_by(user_id=user_id).all()

    # Prepare the response data
    order_list = []
    for order in orders:
        order_data = {
            'order_id': order.id,
            'pickup_location': order.pickup_location,
            'destination': order.destination,
            'comfortability': order.comfortability,
            'pickup_datetime': order.pickup_datetime
        }
        order_list.append(order_data)

    return jsonify({'orders': order_list}), 200

# this is the cancel order route


@app.route('/cancel_order', methods=['GET', 'DELETE'])
@use_args({
    'order_id': fields.Int(validate=validate.Range(min=1), required=True, error_messages={'required': 'The order_id field is required'})}, location='query')
def cancel_order(data):

    order_id = data['order_id']
    # Query the database for the booking with the given ID
    order_id = int(data['order_id'])
    order = Order.query.filter_by(id=order_id).first()

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
