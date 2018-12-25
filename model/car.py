from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
import model.base
from validator import Checker

class Car(model.base.Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key = True)
    reg = Column(String(7), nullable = False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates = 'cars')
    reservations = relationship('Reservation', back_populates = "car")

    reg_rules = Checker()
    reg_rules.add_rule(lambda r: len(r) == 6)
    reg_rules.add_rule(lambda r: all(x.isdigit() for x in r[-3:]))
    reg_rules.add_rule(lambda r: all(x.isalpha() for x in r[:3]))


    def __init__(self, reg):
        self.reg = reg
        
    @property
    def link(self):
        return '{}/cars/{}'.format(self.customer.link, self.id)

    @validates('reg')
    def validate_reg(self, key, reg):
        if not self.reg_rules.validate(reg):
            raise ValueError('Reg number must be in the format ABC123')
        return reg

    def to_json(self):
        result = {'href': self.link}
        result = {**result, **{k: v for k, v in self.__dict__.items()}}
        result['links'] = [{'rel': 'reservations', 'href': '{}/reservations'.format(self.link)}]
        del result['_sa_instance_state']
        del result['customer']
        return result
       
    def __repr__(self):
        parameters = ', '.join([str(v) for v in self.__dict__.values()])
        return '{}({})'.format(self.__class__.__name__, parameters)

    def __str__(self):
        return 'Car({}, {})'.format(self.id, self.reg)

    def __eq__(self, other):
        return self.reg == other.reg

