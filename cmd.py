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
    parser.add_argument('-clean', nargs='?', help='Removes database file')
    parser.add_argument('-create', nargs='?', help='Creates database with tables')
    parser.add_argument('-drop', nargs='?', help='Empties database tables')
    parser.add_argument('-structure', nargs='?', help='Prints table structure')
    
    args = parser.parse_args()

    if args.clean is not None:
        print(args.clean)
        if os.path.exists(config.db_name):
            os.remove(config.db_name)
    if args.create:
        commands.create()
    elif args.drop:
        commands.drop_tables()
    elif args.structure:
        commands.structure()
