from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
import model.base

class Driver(model.base.Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

    def __init__(self, name):
        self.name = name

    @property
    def link(self):
        return '/api/drivers/{}'.format(self.id)

    def to_json(self):
        result = {'href': self.link}
        result = {**result, **{k: v for k, v in self.__dict__.items()}}
        del result['_sa_instance_state']
        return result

    def __repr__(self):
        parameters = ', '.join([str(v) for v in self.__dict__.values()])
        return '{}({})'.format(self.__class__.__name__, parameters)

    def __str__(self):
        return 'Driver({}, {})'.format(self.id, self.name)