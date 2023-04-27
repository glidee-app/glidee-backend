from flask import request, jsonify, abort
from models import db, User, TokenBlacklist
from verification.email_verification import EmailAuthentication
from send_token import Token
from flask import Flask



# Initialize the Flask application
app = Flask(__name__)

# Configure the Flask app to use a SQLite database using Flask SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
token=Token()
new_token=token.confirm_token()
# Define the routes for the Flask app

# Define the routes for the Flask app
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome', 'authentication_endpoints': {"signup": '/signup/<username>/<email>/<password>/<confirm_password>', "signin": '/signin/<username_or_email>/<password>', }}), 201

@app.route('/signup/<username>/<email>/<password>/<confirm_password>', methods=['GET', 'POST'])
def signup(username, email, password, confirm_password):
    db.create_all()

    email_authentication=EmailAuthentication(username=username, email=email)

    if not username or not email or not password or not confirm_password:
        return jsonify({'message': 'Please enter all required information.'}), 400

    if not email_authentication.validate_email_payload():
        return jsonify({'message': 'Please enter a valid username and email'}), 400


    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'That username or email already exists. Please choose another.'}), 400

    if password !=confirm_password:
        return jsonify({'message': 'The passwords you entered do not match. Please make sure that both passwords are the same.'}), 400


    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': f'User {username} successfully registered.'}), 201

@app.route('/signin/<username_or_email>/<password>', methods=['GET', 'POST'])
def signin(username_or_email, password):
    if not username_or_email or not password:
        return jsonify({'message': 'Please enter your username or email and password.'}), 400

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid login credentials. Please try again.'}), 401

    auth_token = user.encode_auth_token(user.id)
    return jsonify({'message': f'Welcome back, {user.username}.'}), 200


@app.route('/forgot_password/<email>', methods=['GET','POST'])
def forgot_password(email):
    if not email:
        return jsonify({'message': 'Please enter your email.'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid email. Please try again.'}), 401

    reset_token = token.send_token(email=email)
    

    # Here you would send an email to the user containing the reset token
    # You could use a service like SendGrid or Mailgun to handle this

    return jsonify({'message': 'An email containing instructions to reset your password has been sent.'}), 200

@app.route('/reset_password/<email>/<token>/<new_password>', methods=['GET', 'POST'])
def reset_password(email, token, new_password):
    if not email:
        return jsonify({'message': 'Please enter your email.'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid email. Please try again.'}), 401

    if token != new_token:
        return jsonify({'message': 'Invalid Token. Please try again.'}), 401

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid email. Please try again.'}), 401

    if not new_password:
        return jsonify({'message': 'Please enter your new password.'}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password successfully changed.'}), 200


if __name__=="__main__":
    app.run(debug=True)
