#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
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
        return {'error': 'who?'}, 404
    return owner.to_dict(rules=('-cars.dealer_id', '-cars.dealer', '-cars.owner_id')), 200

@app.get('/dealerships')
def all_dealers():
    dealer = Dealership.query.all()
    return [d.to_dict(rules=('-cars', '-owner')) for d in dealer], 200

@app.get('/dealerships/<int:id>')
def dealer_by_id(id):
    dealer = db.session.get(Dealership, id)
    if not dealer:
        return {'error': 'out of business!'}, 404
    return dealer.to_dict(rules=('-cars', '-owner')), 200

@app.get('/cars')
def all_cars():
    cars = Car.query.all()
    return [c.to_dict(rules=('-dealer_id', '-owner_id',)) for c in cars], 200

@app.get('/cars/<ind:id')
def get_car_by_id(id):
    car = db.session.get(Car, id)
    if not car:
        return {'error': 'no such car!'}, 404
    return car.to_dict(rules=('-dealer_id', '-owner_id',)), 200
        

@app.delete('/cars/<int:id>')
def delete_car(id):
    car = db.session.get(Car, id)
    if not car:
        return {'error': 'no car? stolen? sold?'}, 404
    db.session.delete(car)
    db.session.commit()
    return {}, 204

@app.delete('/owners/<int:id>')
def delete_owner(id):
    owner = db.session.get(Owner, id)
    if not owner:
        return {'error': 'who?'}, 404
    db.session.delete(owner)
    db.session.commit()
    return {}, 204

@app.delete('/dealerships/<int:id>')
def delete_dealer(id):
    dealer = db.session.get(Dealership, id)
    if not dealer:
        return {'error': 'already went bankrupt'}, 404
    db.session.delete(dealer)
    db.session.commit()
    return {}, 204

@app.post('/cars')
def post_car():
    try:
        data = request.json
        car = Car(
            make = data['make'],
            model = data['model'],
            date_sold=data["date_sold"],
            owner_id = data['owner_id'],
            dealer_id = data['dealer_id']
        )
        db.session.add(car)
        db.session.commit()
        return car.to_dict(rules=('-dealer_id', '-owner_id',)), 201
    except Exception as e:
        raise ValueError({'error': f'Shumting Wong! {e}'})
    
@app.post('/owners')
def post_owner():
    try:
        data = request.json
        owner = Owner(
            first_name = data['first_name'],
            last_name = data['last_name']
        )
        db.session.add(owner)
        db.session.commit()
        return owner.to_dict(), 201
    except:
        return {'error': 'Shumting Wong!'}, 406
    
@app.post('/dealerships')
def post_dealer():
    try:
        data = request.json
        deal = Dealership(
            name = data['name'],
            address = data['address']
        )
        db.session.add(deal)
        db.session.commit()
        return deal.to_dict(), 201
    except:
        return {'error': 'Shumting Wong!'}, 406

@app.patch('/owners/<int:id>')
def patch_owner(id):
    owner = db.session.get(Owner, id)
    if not owner:
        return {'error': 'who?'}, 404
    try:
        data = request.json
        for key in data:
            setattr(owner, key, data[key])
        db.session.add(owner)
        db.session.commit()
        return owner.to_dict(), 201
    except Exception as e:
        return {'error': f'Shumting Wong! {e}'}, 406
    
@app.patch('/dealerships/<int:id>')
def patch_deal(id):
    deal = db.session.get(Dealership, id)
    if not deal:
        return {'error': 'Wrong place!'}, 404
    try:
        data = request.json
        for key in data:
            setattr(deal, key, data[key])
        db.session.add(deal)
        db.session.commit()
        return deal.to_dict(), 201
    except Exception as e:
        return {'error': f'Shumting Wong! {e}'}, 406
    
@app.patch('/cars/<int:id>')
def patch_car(id):
    car = db.session.get(Car, id)
    if not car:
        return {'error': 'Wrong!'}, 404
    try:
        data = request.json
        for key in data:
            setattr(car, key, data[key])
        db.session.add(car)
        db.session.commit()
        return car.to_dict(), 201
    except Exception as e:
        return {'error': f'Shumting Wong! {e}'}, 406

if __name__ == '__main__':
    app.run(port=5555, debug=True)


