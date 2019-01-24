from contextlib import contextmanager
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from model.car import Car
from model.customer import Customer
from model.reservation import Reservation
from model.driver import Driver
from model.user import User

class MyDb():
    def __init__(self, uri):
        self.engine = create_engine(uri)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.session.commit()

    def add(self, item):
        self.session.add(item)

    def delete(self, item):
        self.session.delete(item)

    def cars(self):
        return self.session.query(Car).join(Customer).all()

    def car(self, customer_id, car_id):
        return self.session.query(Car).filter_by(id=car_id, customer_id=customer_id).first()

    def customers(self):
        return self.session.query(Customer).all()

    def customer(self, customer_id):
        return self.session.query(Customer).filter_by(id=customer_id).first()

    def reservations(self):
        return self.session.query(Reservation).all()

    def reservation(self, reservation_id):
        return self.session.query(Reservation).filter_by(id=reservation_id).first()

    def reservations_for(self, customer_id):
        return self.session.query(Reservation).filter(Reservation.car.has(customer_id=customer_id)).all()

    def drivers(self):
        return self.session.query(Driver).all()

    def driver(self, driver_id):
        return self.session.query(Driver).filter_by(id=driver_id).first()

    def users(self):
        return self.session.query(User).all()

    def user(self, user_id):
        return self.session.query(User).filter_by(id=user_id).first()
