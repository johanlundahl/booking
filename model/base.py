from sqlalchemy.ext.declarative import declarative_base

class ModelBase():
    def __repr__(self):
        parameters = ', '.join([str(v) for v in self.__dict__.values()])
        return 'BASE {}({})'.format(self.__class__.__name__, parameters)

    @classmethod
    def valid_create(cls, dict):
        required = cls.__init__.__code__.co_varnames
        return all(k in dict.keys() for k in required if k not in ['self', 'new_state'])

    @classmethod
    def valid_update(cls, dict):
        required = cls.__init__.__code__.co_varnames
        return any(k in dict.keys() for k in required if k not in ['self', 'new_state'])

    @classmethod
    def create(cls, dict):
        return cls(**dict)

    def update(self, dict):
        [setattr(self, k, v) for k, v in dict.items()]

Base = declarative_base(cls = ModelBase)