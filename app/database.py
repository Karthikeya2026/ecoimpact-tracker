from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    inputs = db.relationship('Input', backref='user', lazy=True)

class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    energy_kwh = db.Column(db.Float, nullable=False)
    miles_driven = db.Column(db.Float, nullable=False)
    waste_kg = db.Column(db.Float, nullable=False)
    emissions = db.Column(db.Float, nullable=False)