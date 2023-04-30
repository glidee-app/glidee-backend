from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Integer, Column, ForeignKey, String
import jwt

db = SQLAlchemy()

# Define the User model for the database
class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                algorithm='HS256',
                key="dami"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def generate_password_reset_token(email):
        try:
            # Create a payload with the user's ID and a timestamp
            payload = {
                'user_email': email,
                'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }

            # Encode the payload as a JWT token
            token = jwt.encode(payload, algorithm='HS256')

            # Return the token as a string
            return token.decode('utf-8')
        except Exception as e:
            return e

class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token = db.Column(db.String(500), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, token):
        self.jti = jti
        self.token = token
        self.expires_at = datetime.utcnow() + timedelta(days=7)

    @classmethod
    def is_token_blacklisted(cls, jti):
        token = cls.query.filter_by(jti=jti).first()
        return bool(token and token.expires_at > datetime.utcnow())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
