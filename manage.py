import argparse
import json
from random import sample, randint

from sweet_grany_app.sql_service import SQLService
from sweet_grany_app.core_service import CoreService
from sweet_grany_app.models.orm_models import Base
from sweet_grany_app.orm_service import ORMService
from sweet_grany_app.models.core_models import meta_object
from config import QUERIES_PATH
from utils.db_data_generator import (
    Author, AUTHORS,
    Tag, TAGS,
    Shop, SHOPS,
    Products, PRODUCTS,
    Recipe, COOKING_WORDS,
    DataGenerator, ADVERBS
)

query_path = QUERIES_PATH


def get_db_worker(worker_type: str):
    workers_type_mapping = {
        'sql': {
            'class': SQLService,
            'args': ('postgresql://localhost:5432',
                     'sweet_granny',
                     query_path)
        },
        'core': {
            'class': CoreService,
            'args': ('postgresql://localhost:5432',
                     'sweet_granny',
                     meta_object)
        },
        'orm': {
            'class': ORMService,
            'args': ('postgresql://localhost:5432',
                     'sweet_granny',
                     Base)
        }
    }
    worker_class = workers_type_mapping[worker_type]['class']
    args = workers_type_mapping[worker_type]['args']
    return worker_class(*args)


def create_tables(worker):
    sql_service = get_db_worker(worker)
    sql_service.create_all_tables()


def drop_tables(worker):
    sql_service = get_db_worker(worker)
    sql_service.drop_all_tables()


def recreate_tables(worker):
    sql_service = get_db_worker(worker)
    sql_service.drop_all_tables()
    sql_service.create_all_tables()


def fill_in_tables(worker):
    """
    Fill in tables in the next order:
    1. authors
    2. tags
    3. products
    4. shops
    5. recipes
    :return: None
    """
    db_data = json.loads(read_file('db_data.json'))
    sql_service = get_db_worker(worker)
    sql_service.fill_in_authors(db_data['authors'])
    sql_service.fill_in_products(db_data['products'])
    sql_service.fill_in_shops(db_data['shops'])
    sql_service.fill_in_recipes(db_data['recipes'])
    # sql_service.fill_in_authors(Author(AUTHORS).get_all_authors())
    # sql_service.fill_in_products(Products(PRODUCTS).get_all_products_names())
    # sql_service.fill_in_shops(
    #     list(Shop(SHOPS, PRODUCTS).get_shop_data_generator())
    # )
    # sql_service.fill_in_recipes(
    #     [DataGenerator(
    #         Tag(TAGS),
    #         Author(AUTHORS),
    #         Products(PRODUCTS),
    #         Shop(SHOPS, PRODUCTS),
    #         Recipe(
    #             COOKING_WORDS['cooking']['clean'],
    #             COOKING_WORDS['cooking']['prepare'],
    #             COOKING_WORDS['cooking']['merge'],
    #             COOKING_WORDS['cooking']['cook'],
    #             COOKING_WORDS['cooking']['finalize'],
    #             ADVERBS,
    #             sample(PRODUCTS, randint(3, 5))
    #         )
    #     ).generate_recipe() for _ in range(50)]
    # )


def generate_db_data(file='db_data.json'):
    db_data = {
        'authors': Author(AUTHORS).get_all_authors(),
        'products': Products(PRODUCTS).get_all_products_names(),
        'shops': list(Shop(SHOPS, PRODUCTS).get_shop_data_generator()),
        'recipes': [DataGenerator(
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
        ).generate_recipe() for _ in range(50)]
    }
    write_file(file, json.dumps(db_data))
    print(f'data generated in {file}')


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
        'gen_data': generate_db_data
    }
    parser = argparse.ArgumentParser(
        description='Main module to rule dbs'
    )
    parser.add_argument('action', choices=actions.keys())
    parser.add_argument('-db', '--db_type', default='sweet_granny')
    parser.add_argument('-w', '--worker',
                        choices=['sql', 'core', 'orm'])

    args = parser.parse_args()

    if args.action in ('create', 'drop', 'recreate', 'fill_in'):
        actions[args.action](args.worker)
    elif args.action in ('gen_data',):
        actions[args.action]()
