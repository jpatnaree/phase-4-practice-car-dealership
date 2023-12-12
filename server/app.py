#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Dealership, Owner, Car

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

@app.get('/owners')
def all_owners():
    owner = Owner.query.all()
    return [o.to_dict(rules=('-cars', '-dealer',)) for o in owner], 200

@app.get('/owners/<int:id>')
def owner_by_id(id):
    owner = db.session.get(Owner, id)
    if not owner:
        return {'error': 'who?'}
    return owner.to_dict(rules=('-cars.dealer_id', '-cars.dealer', '-cars.owner_id')), 200

@app.delete('/owners/<int:id>')
def delete_owner(id):
    owner = db.session.get(Owner, id)
    if not owner:
        return {'error': 'who?'}
    db.session.delete(owner)
    db.session.commit()
    return {}, 204

@app.get('/dealerships')
def all_dealers():
    dealer = Dealership.query.all()
    return [d.to_dict(rules=('-cars', '-owner')) for d in dealer], 200

@app.get('/dealerships/<int:id>')
def dealer_by_id(id):
    dealer = db.session.get(Dealership, id)
    if not dealer:
        return {'error': 'out of business!'}
    return dealer.to_dict(rules=('-cars', '-owner')), 200

@app.get('/cars')
def all_cars():
    cars = Car.query.all()
    return [c.to_dict(rules=('-dealer_id', '-owner_id',)) for c in cars], 200

@app.delete('/cars/<int:id>')
def delete_car(id):
    car = db.session.get(Car, id)
    if not car:
        return {'error': 'no car? stolen?'}, 404
    db.session.delete(car)
    db.session.commit()
    return {}, 204

@app.post('/cars')
def post_car():
    data = request.json
    try:
        car = Car(
            make = data['make'],
            model = data['model'],
            owner_id = data['owner_id'],
            dealer_id = data['dealer_id']
        )
        db.session.add(car)
        db.session.commit()
        return car.to_dict(rules=('-owner.id', 'dealer.id',)), 200
    except:
        raise ValueError({'error': 'Shumting Wong!'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
