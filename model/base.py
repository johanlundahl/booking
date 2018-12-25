from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Id():
	def __init__(self):
		self._id = str(id(self))

	@property
	def id(self):
		return self._id
	
	def __repr__(self):
		parameters = ', '.join([str(v) for v in self.__dict__.values()])
		return '{}({})'.format(self.__class__.__name__, parameters)