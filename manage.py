import argparse
import json
from random import sample, randint

from sweet_grany_app.sql_service import SQLService
from sweet_grany_app.core_service import CoreService
from sweet_grany_app.models.orm_models import Base
from sweet_grany_app.orm_service import ORMService
from sweet_grany_app.models.core_models import meta_object
from config import DB_NAME, DB_URL
from utils.db_data_generator import (
    Author, AUTHORS,
    Tag, TAGS,
    Shop, SHOPS,
    Products, PRODUCTS,
    Recipe, COOKING_WORDS,
    DataGenerator, ADVERBS
)


def get_db_worker(worker_type: str):
    workers_type_mapping = {
        'sql': {
            'class': SQLService,
            'args': (DB_URL, DB_NAME,)
        },
        'core': {
            'class': CoreService,
            'args': (DB_URL, DB_NAME, meta_object)
        },
        'orm': {
            'class': ORMService,
            'args': (DB_URL, DB_NAME, Base)
        }
    }
    worker_class = workers_type_mapping[worker_type]['class']
    args = workers_type_mapping[worker_type]['args']
    return worker_class(*args)


def create_tables(worker):
    sql_service = get_db_worker(worker)
    sql_service.create_tables()


def drop_tables(worker):
    sql_service = get_db_worker(worker)
    sql_service.drop_tables()


def recreate_tables(worker):
    sql_service = get_db_worker(worker)
    sql_service.drop_tables()
    sql_service.create_tables()


def fill_in_tables(worker, file='db_data.json'):
    """
    Fill in tables in the next order:
    1. authors
    2. tags
    3. products
    4. shops
    5. recipes
    :return: None
    """
    db_data = json.loads(read_file(file))
    sql_service = get_db_worker(worker)
    sql_service.fill_authors(db_data['authors'])
    sql_service.fill_products(db_data['products'])
    sql_service.fill_shops(db_data['shops'])
    sql_service.fill_recipes(db_data['recipes'])


def generate_db_data(file='db_data.json'):
    data_generator = DataGenerator(
        Tag(TAGS),
        Author(AUTHORS),
        Products(PRODUCTS),
        Shop(SHOPS, PRODUCTS),
        Recipe(
            COOKING_WORDS['cooking']['clean'],
            COOKING_WORDS['cooking']['prepare'],
            COOKING_WORDS['cooking']['merge'],
            COOKING_WORDS['cooking']['cook'],
            COOKING_WORDS['cooking']['finalize'],
            ADVERBS,
            sample(PRODUCTS, randint(3, 5))
        )
    )
    db_data = {
        'authors': data_generator.generate_authors(),
        'products': data_generator.generate_products(),
        'shops': data_generator.generate_shops(),
        'recipes': data_generator.generate_recipes(50)
    }
    write_file(file, json.dumps(db_data))
    print(f'data generated in {file}')


def get_recipe_prices(worker, title):
    sql_service = get_db_worker(worker)
    print(sql_service.get_recipe_costs(title))


def get_components_prices(worker, title):
    sql_service = get_db_worker(worker)
    data = sql_service.get_components_price(title)
    template = '{:^20}' * 5
    titles = ('PRODUCT', 'SHOP', 'PRICE', 'WEIGHT', 'COST')
    print(template.format(*titles), '\n')
    for item in data:
        print(template.format(*item))



def write_file(file, data):
    with open(file, 'w') as file:
        file.write(data)


def read_file(file):
    with open(file, 'r') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    actions = {
        'create': create_tables,
        'drop': drop_tables,
        'recreate': recreate_tables,
        'fill_in': fill_in_tables,
        'gen_data': generate_db_data,
        'rec_prc': get_recipe_prices,
        'cmp_prc': get_components_prices
    }
    parser = argparse.ArgumentParser(
        description='Main module to rule dbs.\n'
                    'If you run for the first time - you have to create file '
                    'with data for tables. Use "gen_data" action for it',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'action', type=str, choices=actions.keys(),
        help='create - create all tables if not exists,\n'
             'drop - drop all tables if exists,\n'
             'recreate - drop -> create all tables\n\n'
             '!!!create, drop, recreate requires -w param.\n\n'
             'gen_data - generate data for db tables to file "db_data.json", '
             'doesn\'t require for additional params\n\n'
             'rec_prc - returns max and min prices for recipe by title\n'
             '!!! requires: "-w" param, "-t" - recipe title\n\n'
             'cmp_prc - returns cheaper prices for recipe components'
             '!!! requires: "-w" param, "-t" - recipe title\n\n'
    )
    parser.add_argument(
        '-db', '--database', type=str, default='sweet_granny',
        help='define data base name'
    )
    parser.add_argument(
        '-w', '--worker', choices=['sql', 'core', 'orm'],
        help='define worker type'
    )
    parser.add_argument(
        '-t', '--title',
        help='recipe title'
    )

    args = parser.parse_args()

    if args.action in ('create', 'drop', 'recreate', 'fill_in'):
        actions[args.action](args.worker)
    elif args.action in ('gen_data',):
        actions[args.action]()
    elif args.action in ('rec_prc', 'cmp_prc'):
        actions[args.action](args.worker, args.title)
