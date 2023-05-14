from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        return create_access_token({
            'user_id': self.id,
            'user_name': f'{self.first_name} {self.last_name}'
        })


class Driver(db.Model):
    __tablename__ = "drivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    vehicles = db.relationship('Vehicle', backref='driver', lazy=True)


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    license_plate = db.Column(db.String(20), nullable=False)
    comfortability = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey(
        'drivers.id'), nullable=False)
    orders = db.relationship(
        'Order', back_populates='vehicle', foreign_keys="Order.vehicle_id", lazy=True)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey(
        'drivers.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.id'), nullable=False)
    vehicle = db.relationship(
        'Vehicle', foreign_keys="Order.vehicle_id", back_populates='orders')

    comfortability = db.Column(db.String(50), db.ForeignKey(
        'vehicles.comfortability'), nullable=False)
    amount = db.Column(db.Integer, db.ForeignKey(
        'vehicles.amount'), nullable=False)
    pickup_datetime = db.Column(db.DateTime, nullable=False)
    pickup_location = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)

    # 1 represents active while 0 represents cancelled
    status = db.Column(db.Integer, nullable=False, default=1)
