from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from db.orm import MyDb
from model.base import Base
from model.car import Car
from model.customer import Customer
from model.reservation import Reservation
from model.driver import Driver
import config

uri = config.db_uri

def get_engine():
    return create_engine(uri)

def get_inspector():
    engine = get_engine()
    return inspect(engine)

def structure():
    inspector = get_inspector()
    for table in inspector.get_table_names():
        print('Table {}'.format(table))
        for column in inspector.get_columns(table):
            print('  Column {} ({})'.format(column['name'], column['type']))

def create():
    engine = get_engine()
    Base.metadata.create_all(engine)

def drop_tables():
    engine = get_engine()
    Base.metadata.drop_all(engine)

def table_size():
    with MyDb(uri) as my_db: 
        ps = my_db.persons()
        print('Table person: {}'.format(len(ps)))

if __name__ == '__main__':
    print('MAIN')