from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.orm import declarative_base
import jwt


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            algorithm='HS256',
            key='some-random-key'
        )

    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token,
                key='some-random-key'
            )
            return payload.get('sub')
        except jwt.ExpiredSignatureError:
            raise Exception('Token expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token. Please log in again.')

    # Not used for now

    # def generate_password_reset_token(email):
    #     try:
    #         # Create a payload with the user's ID and a timestamp
    #         payload = {
    #             'user_email': email,
    #             'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #         }

    #         # Encode the payload as a JWT token
    #         token = jwt.encode(payload, algorithm='HS256')

    #         # Return the token as a string
    #         return token.decode('utf-8')
    #     except Exception as e:
    #         return e
