# http://blog.tecladocode.com/learn-python-defining-user-access-roles-in-flask/

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship, validates
import model.base
from passlib.hash import pbkdf2_sha256 as sha256

ACCESS_LEVEL = {'none': 0, 'user': 1, 'admin': 2}

class User(model.base.Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(100), nullable = False)
    password = Column(String(100), nullable = False)
    access_level = Column(Integer, nullable = False)

    def __init__(self, name, email, password, access_level=ACCESS_LEVEL['none']):
        self.name = name
        self.email = email
        self.password = password
        self.access_level = access_level

    @validates('password')
    def validate_password(self, key, password):
        print('Setting password...')
        return sha256.hash(password)

    def authenticate(self, password):
        return sha256.verify(password, self.password)

    def authorize(self, access_level):
        return self.access_level >= access_level

    def to_json(self):
        result = {'href': '/api/users/{}'.format(self.id)}
        result = {**result, **{k: v for k, v in self.__dict__.items()}}
        del result['_sa_instance_state']
        return result

    def __str__(self):
        return 'User({}, {}, {})'.format(self.id, self.name, self.access_level)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id