from models import User, Driver, Order, Vehicle, db, Ride
from flask import Flask, render_template, jsonify
from webargs import fields, validate
from webargs.flaskparser import use_args
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from send_token import Token
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'some-secret-key')

jwt = JWTManager(app)
db.init_app(app)
CORS(app, origins=['http://localhost:3000'])


token = Token()
new_token = token.confirm_token()


# home route
@app.get('/')
def index():
    db.create_all()
    return render_template("index.html")



@app.route('/seed_drivers', methods=["GET", "POST"])
def seed_drivers():
    drivers = [
        ('Michael Jordans', '1234567890', 'michaeljordans@example.com'),
        ('Jane Smith', '9876543210', 'janesmith@example.com'),
        ('Michael Johnson', '5678901234', 'michaeljohnson@example.com'),
        ('Emily Davis', '4321098765', 'emilydavis@example.com'),
        ('Daniel Wilson', '9876543210', 'danielwilson@example.com'),
        ('Sarah Brown', '1234567890', 'sarahbrown@example.com'),
        ('Christopher Lee', '9876543210', 'christopherlee@example.com'),
        ('Jessica Miller', '5678901234', 'jessicamiller@example.com'),
        ('Matthew Taylor', '4321098765', 'matthewtaylor@example.com'),
        ('Olivia Anderson', '9876543210', 'olivianderson@example.com')
    ]

    try:
        for driver in drivers:
            db.session.add(Driver(name=driver[0], phone_number=driver[1], email=driver[2]))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error occurred while seeding drivers. {e}'}), 500

    return jsonify({'message': 'Drivers seeded successfully.'}), 200


# Route to seed the data into the database
@app.route('/seed_vehicles', methods=["GET", "POST"])
def seed_vehicles():
    # Insert vehicles
    vehicles =[
                {
                "make": "Toyota",
                "model": "Camry",
                "license_plate": "ABC123",
                "comfortability": "Standard",
                "amount": 60,
                "driver_id": 1
                },
                {
                "make": "Honda",
                "model": "Accord",
                "license_plate": "XYZ456",
                "comfortability": "Shared",
                "amount": 40,
                "driver_id": 2
                },
                {
                "make": "Ford",
                "model": "F-150",
                "license_plate": "DEF789",
                "comfortability": "Shared",
                "amount": 50,
                "driver_id": 3
                },
                {
                "make": "Chevrolet",
                "model": "Cruze",
                "license_plate": "GHI012",
                "comfortability": "Standard",
                "amount": 80,
                "driver_id": 4
                },
                {
                "make": "BMW",
                "model": "X5",
                "license_plate": "JKL345",
                "comfortability": "Standard",
                "amount": 100,
                "driver_id": 5
                },
                {
                "make": "Nissan",
                "model": "Altima",
                "license_plate": "MNO678",
                "comfortability": "Standard",
                "amount": 70,
                "driver_id": 6
                },
                {
                "make": "Audi",
                "model": "A4",
                "license_plate": "PQR901",
                "comfortability": "Standard",
                "amount": 90,
                "driver_id": 7
                },
                {
                "make": "Volkswagen",
                "model": "Golf",
                "license_plate": "STU234",
                "comfortability": "Standard",
                "amount": 110,
                "driver_id": 8
                },
                {
                "make": "Mercedes-Benz",
                "model": "C-Class",
                "license_plate": "VWX567",
                "comfortability": "Shared",
                "amount": 30,
                "driver_id": 9
                },
                {
                "make": "Hyundai",
                "model": "Elantra",
                "license_plate": "YZA890",
                "comfortability": "Shared",
                "amount": 20,
                "driver_id": 10
                },
                {
                "make": "Chevrolet",
                "model": "Malibu",
                "license_plate": "BCD123",
                "comfortability": "Standard",
                "amount": 130,
                "driver_id": 1
                },
                {
                "make": "Honda",
                "model": "Civic",
                "license_plate": "EFG456",
                "comfortability": "Standard",
                "amount": 150,
                "driver_id": 2
                },
                {
                "make": "Toyota",
                "model": "Corolla",
                "license_plate": "HIJ789",
                "comfortability": "Standard",
                "amount": 170,
                "driver_id": 3
                },
                {
                "make": "BMW",
                "model": "3 Series",
                "license_plate": "KLM012",
                "comfortability": "Standard",
                "amount": 190,
                "driver_id": 4
                }
                    ]

    for vehicle in vehicles:
        new_vehicle = Vehicle(
            make=vehicle['make'],
            model=vehicle['model'],
            license_plate=vehicle['license_plate'],
            comfortability=vehicle['comfortability'],
            amount=vehicle['amount'],
            driver_id=vehicle['driver_id']
        )
        db.session.add(new_vehicle)

    db.session.commit()

    return jsonify({'message': 'Data seeded successfully.'}), 200

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
        email=data['email'].lower()
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
        .filter((User.email == data['email'].lower()))
        .first()
    )
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid login credentials.'}), 400

    try:
        auth_token = user.generate_auth_token()
    except Exception:
        return jsonify({'message': 'Error occured.'}), 500

    return jsonify({
        'message': 'User logged in successfully.',
        'data': {'token': auth_token}
    }), 200


# Forgot email route
@app.post('/forgot_password')
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


@app.get('/rides')
@jwt_required()
@use_args({
    'comfortability': fields.Str(validate=validate.OneOf(['standard', 'premium']), required=True, error_messages={'required': 'The comfortability field is required'}),
    'pickup_date': fields.Date(format='%Y-%m-%d', required=True, error_messages={'required': 'The pickup_datetime field is required'}),
    'pickup_location': fields.Str(required=True, error_messages={'required': 'The pickup_location field is required'}),
    'destination': fields.Str(required=True, error_messages={'required': 'The destination field is required'}),
}, location='query')
def fetch_rides(data):
    rides_model = (
        Ride.query.join(Ride.vehicle)
        .filter(Vehicle.comfortability == data['comfortability'])
        .filter(Ride.pickup_date == data['pickup_date'])
        .filter(Ride.pickup_location == data['pickup_location'])
        .filter(Ride.destination == data['destination'])
        .filter(Ride.is_booked == False)
        .all()
    )

    rides = []
    for ride_model in rides_model:
        rides.append({
            'id': ride_model.id,
            'amount': ride_model.vehicle.amount,
            'vehicle': {
                'make': ride_model.vehicle.make,
                'model': ride_model.vehicle.model,
                'license_plate': ride_model.vehicle.license_plate,
                'comfortability': ride_model.vehicle.comfortability,
            },
            'driver': {
                'id': ride_model.vehicle.driver_id,
                'name': ride_model.vehicle.driver.name,
            },
            'pickup_time': ride_model.pickup_time,
        })

    return jsonify({
        'data': {'rides': rides},
        'message': 'Rides fetched successully'
    }), 200


@app.post('/create_order')
@jwt_required()

@use_args({
    'ride_id': fields.Int(required=True, validate=validate.Range(min=1), error_messages={'required': 'The vehicle_id field is required'}),
}, location='json')

def create_order(data):

    user = get_jwt_identity()

    ride = Ride.query.filter_by(
        id=data['ride_id']).first()

    if not ride:
        return jsonify({'message': 'Invalid ride ID'}), 400

    ride.is_booked == True

    order = Order(
        user_id=user['user_id'],
        ride_id=data['ride_id'],
        status = 'upcoming_trip'
    )

    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@app.post('/cancel_order')
@jwt_required()
@use_args({
    'order_id': fields.Int(validate=validate.Range(min=1), required=True, error_messages={'required': 'The order_id field is required'}),
    'ride_id': fields.Int(required=True, validate=validate.Range(min=1), error_messages={'required': 'The vehicle_id field is required'})
    }, location='json')


def cancel_order(data):
    user = get_jwt_identity()
    
    ride_id = data['ride_id']
    order = Order.query.filter_by(
        id=data['order_id'],
        user_id=user['user_id']
    ).first()

    if not order:
        return jsonify({'message': 'Invalid order ID'}), 400

    ride = Ride.query.get(ride_id)
    if ride: 
        ride.is_booked = False # make ride available again so it can be booked

    order.status = 'cancelled_order'  
    db.session.commit()

    return jsonify({'message': 'Order cancelled successfully'}), 200


@app.get('/order_history')
@jwt_required()

@use_args({
    'status': fields.Str(validate=validate.OneOf(['upcoming_trip', 'completed_trip', 'cancelled_trip']), required=True, error_messages={'required': 'The status field is required'})
}, location='query')

def get_user_orders(data):
    order_status= data['status']

    user = get_jwt_identity()


    order_models = (
        Order.query
        .filter_by(user_id=user['user_id'])
        .filter_by(status = order_status)
        .order_by(Order.created_at)
        .all()
    )
    orders = []

    for order_model in order_models:
        if order_model.status == order_status:
            orders.append({
                'id': order_model.id,
                'pickup_location': order_model.ride.pickup_location,
                'destination': order_model.ride.destination,
                'pickup_time': order_model.ride.pickup_time,
                'amount': order_model.ride.amount,
                'pickup_date': order_model.ride.pickup_date,
                'vehicle': {
                    'id': order_model.ride.vehicle.id,
                    'make': order_model.ride.vehicle.make,
                    'model': order_model.ride.vehicle.make,
                    'license_plate': order_model.ride.vehicle.license_plate,
                    'comfortability': order_model.ride.vehicle.comfortability,
                },
                'status': order_model.status,
            })

            orders[-1]['pickup_date'] = orders[-1]['pickup_date'].isoformat()

    return jsonify({
        'data': {'orders': orders},
        'message': 'Orders fetched successfully'
    }), 200


@jwt.expired_token_loader
@jwt.invalid_token_loader
@jwt.unauthorized_loader
def my_expired_token_callback(jwt_header, jwt_value=None):
    return jsonify({
        'message': 'Unauthorized! Please login and try again.'
    }), 401



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
