from sqlalchemy.ext.declarative import declarative_base


class ModelBase():
    def __repr__(self):
        parameters = ', '.join([str(v) for v in self.__dict__.values()])
        return 'BASE {}({})'.format(self.__class__.__name__, parameters)

    @classmethod
    def validate(cls, dict):
        required = cls.__init__.__code__.co_varnames
        print(required)
        return all(k in dict.keys() for k in required if k not in ['self', 'new_state'])

    @classmethod
    def create(cls, dict):
        return cls(**dict)

    def update(self, dict):
        [setattr(self, k, v) for k, v in dict.items()]

Base = declarative_base(cls = ModelBase)
#Base = declarative_base()

class Id():
	def __init__(self):
		self._id = str(id(self))

	@property
	def id(self):
		return self._id
	
	def __repr__(self):
		parameters = ', '.join([str(v) for v in self.__dict__.values()])
		return '{}({})'.format(self.__class__.__name__, parameters)


