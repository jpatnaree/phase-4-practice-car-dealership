from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import date, datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owner_table'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    
    serialize_rules = ('-cars.owner',)
    
    cars = db.relationship('Car', back_populates='owner', cascade='all, delete-orphan')
    dealer = association_proxy('cars', 'owner')
    
class Car(db.Model, SerializerMixin):
    __tablename__ = 'car_table'
    
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    date_sold = db.Column(db.Date, nullable=False)
    
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealership_table.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('owner_table.id'))
    
    serialize_rules = ('-owner.cars', '-dealer.cars')
    
    owner = db.relationship('Owner', back_populates='cars')
    dealer = db.relationship('Dealership', back_populates='cars')
    
class Dealership(db.Model, SerializerMixin):
    __tablename__ = 'dealership_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    
    serialize_rules = ('-cars.dealer',)
    
    cars = db.relationship('Car', back_populates='dealer', cascade='all, delete-orphan')
    owner = association_proxy('cars', 'owner')