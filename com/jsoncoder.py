from json import JSONEncoder
from model.customer import Customer
from model.car import Car
from model.reservation import Reservation
from model.driver import Driver
from model.user import User

class Encoder(JSONEncoder):
    
    def default(self, o):
        if any(type(o) is x for x in [Customer, Car, Reservation, Driver, User]):
            return o.to_json()
