#!/usr/bin/env python3

from app import app
from models import db, Dealership, Owner, Car
from faker import Faker
from random import randint, choice

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        Dealership.query.delete()
        Owner.query.delete()
        Car.query.delete()
        
        dealer_list = []
        owner_list = []
        car_list = []
        
        for _ in range(10):
            dealer = Dealership(
                name = f'{faker.first_name()} LTD.',
                address = faker.address()
            )
            dealer_list.append(dealer)
            db.session.add(dealer)
            
            owner = Owner(
                first_name = faker.first_name(),
                last_name = faker.last_name()
            )
            owner_list.append(owner)
            db.session.add(owner)
        db.session.commit()
        
        for _ in range(18):
            rand_owner = choice(owner_list)
            rand_dealer = choice(dealer_list)
            car = Car(
                make = faker.last_name(),
                model = faker.last_name(),
                date_sold = faker.date_between(start_date='-5y', end_date='today'),
                dealer = rand_dealer,
                owner = rand_owner
            )
            car_list.append(car)
            db.session.add(car)
        db.session.commit()

        print("Seeding complete!")

        # for _ in range(0,20):
        #     rand_receiver = choice(receiver_list)
        #     rand_giver = choice(giver_list)
        #     gift = Gift(name=faker.name(), price=(randint(1,1000)/100.0), receiver=rand_receiver, giver=rand_giver)
        #     # gift = Gift(name=faker.commerce.product(), 
        #     #             price=faker.commerce.price(), 
        #     #             receiver=choice(receiver_list))
        #     # gifts.append(gift)
        #     db.session.add(gift)
            
        # db.session.commit()