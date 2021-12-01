import argparse

from sweet_grany_app.sql_sevice import SQLService
from config import QUERIES_PATH
from sweet_grany_app.db_data_generator import (
    Author, AUTHORS
)

path = QUERIES_PATH


def create_tables():
    sql_service = SQLService(path)
    sql_service.create_all_tables()


def recreate_tables():
    sql_service = SQLService(path)
    sql_service.drop_all_tables()
    sql_service.create_all_tables()


def fill_in_tables():
    """
    Fill in tables in the next order:
    1. authors
    2. tags
    3. shops
    4. products
    5. recipes
    :return: None
    """
    sql_service = SQLService(path)
    sql_service.fill_in_authors(Author(AUTHORS).get_all_authors())


if __name__ == '__main__':
    actions = {
        'create': create_tables,
        'recreate': recreate_tables,
        'fill_in': fill_in_tables
    }
    parser = argparse.ArgumentParser(
        description='Main module to rule dbs'
    )
    parser.add_argument('action', choices=actions.keys())
    parser.add_argument('-db', '--db_type', default='sweet_granny')
    args = parser.parse_args()
    actions[args.action]()
