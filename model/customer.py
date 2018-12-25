from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
import model.base

class Customer(model.base.Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    company = Column(Boolean, nullable = False)
    contact = Column(String(100), nullable = False)
    phone = Column(String(20), nullable = False)
    email = Column(String(100), nullable = False)
    address = Column(String(100), nullable = False)
    postal_code = Column(String(6), nullable = False)
    city = Column(String(50), nullable = False)
    cars = relationship('Car', back_populates = "customer")


    def __init__(self, name, contact, phone, email, company=True, address='', postal_code='', city=''):
        self.name = name
        self.company = company
        self.contact = contact
        self.phone = phone
        self.email = email
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.id = None
    
    def to_json(self):
        result = {'href': self.link}
        result = {**result, **{k: v for k, v in self.__dict__.items()}}
        result['links'] = [{'rel': 'reservations', 'href': '/api/reservations?customer_id'.format(self.id)}, 
                        {'rel': 'cars', 'href': '{}/cars'.format(self.link)}]
        del result['_sa_instance_state']
        return result

    @property
    def link(self):
        return '/api/customers/{}'.format(self.id)

    def __contains__(self, item):
        item = item.lower()
        return item in self.name.lower() or item in self.contact

    def __str__(self):
        return 'Customer({}, {})'.format(self.id, self.name)
    
    def __repr__(self):
        parameters = ', '.join(['{}={}'.format(k, str(v)) for k, v in self.__dict__.items()])
        return '{}({})'.format(self.__class__.__name__, parameters)