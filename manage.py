import argparse
from random import sample, randint

from sweet_grany_app.sql_sevice import SQLService
from config import QUERIES_PATH
from sweet_grany_app.db_data_generator import (
    Author, AUTHORS,
    Tag, TAGS,
    Shop, SHOPS,
    Products, PRODUCTS,
    Recipe, COOKING_WORDS,
    DataGenerator, ADVERBS
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
    3. products
    4. shops
    5. recipes
    :return: None
    """
    sql_service = SQLService(path)
    sql_service.fill_in_authors(Author(AUTHORS).get_all_authors())
    sql_service.fill_in_tags(Tag(TAGS).get_all_tags())
    sql_service.fill_in_products(Products(PRODUCTS).get_all_products_names())
    sql_service.fill_in_shops(
        list(Shop(SHOPS, PRODUCTS).get_shop_data_generator())
    )
    sql_service.fill_in_recipes(
        [DataGenerator(
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
    )


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
