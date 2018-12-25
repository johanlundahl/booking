# TUTORIAL
# https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/

from sqlalchemy import create_engine
from db.orm import MyDb
from db import commands 
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database commands')
    parser.add_argument('--action', choices=['create', 'drop', 'structure'], help='drops all tables')
    args = parser.parse_args()

    if args.action == 'create':
        commands.create()
    elif args.action == 'drop':
        commands.drop_tables()
    elif args.action == 'structure':
        commands.structure()