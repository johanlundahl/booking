# TUTORIAL
# https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/

from sqlalchemy import create_engine
from db.orm import MyDb
from db import commands 
import argparse
import config
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database commands')
    parser.add_argument('-clean', help='Removes database file', action='store_true')
    parser.add_argument('-create', help='Creates database with tables', action='store_true')
    parser.add_argument('-drop', help='Empties database tables', action='store_true')
    parser.add_argument('-structure', help='Prints table structure', action='store_true')
    args = parser.parse_args()

    if args.clean:
        if os.path.exists(config.db_name):
            os.remove(config.db_name)
            print('Database file removed')
    if args.create:
        commands.create()
        print('Database created')
    if args.drop:
        commands.drop_tables()
        print('Database tables dropped')
    if args.structure:
        commands.structure()
