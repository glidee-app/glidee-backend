from flask import request, jsonify
from database import Database
from models import User
from flask import Flask, render_template
from webargs.flaskparser import use_args
from webargs import fields
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from flask_swagger import swagger


app = Flask(__name__)
load_dotenv()

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
