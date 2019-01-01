from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
import model.base

class Reservation(model.base.Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key = True)
    date = Column(String(10), nullable = False)
    picked_up = Column(Boolean, nullable = False)
    returned = Column(Boolean, nullable = False)
    pickup_at = Column(String(5), nullable = False)
    return_at = Column(String(5), nullable = False)

    car_id = Column(Integer, ForeignKey('cars.id'))
    car = relationship('Car', back_populates = 'reservations')

    pickup_driver = Column(Integer, ForeignKey('drivers.id'))
    pickup_by = relationship('Driver', back_populates = 'pickups')
    
    def __init__(self, date, pickup_at, return_at):
        self.date = date
        self.pickup_at = pickup_at
        self.return_at = return_at
        self.returned = False
        self.picked_up = False
        self.pickup_driver = None

    def to_json(self):
        result = {'href': self.link}
        result = {**result, **{k: v for k, v in self.__dict__.items()}}
        result['customer_id'] = self.customer_id
        del result['_sa_instance_state']
        del result['car']
        return result

    @property
    def customer_id(self):
        return self.car.customer_id

    @property
    def link(self):
        return '/api/customers/{}/cars/{}/reservations/{}'.format(self.customer_id, self.car_id, self.id)
    
    