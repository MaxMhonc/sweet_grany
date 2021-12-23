import os
from typing import Optional

import sqlalchemy.engine
from sqlalchemy import create_engine, text
from sqlalchemy.engine import CursorResult

from sweet_grany_app.service_interface import AbstractService
from sweet_grany_app.models.sql_queries import ddl, dml


class SQLService(AbstractService):
    """SQLService implements DB tables handling via raw SQL queries"""

    def __init__(self, db_url: str, db_name: str):
        self.db_url = db_url
        self.db_name = db_name
        self.engine = self._create_engine()

    def create_tables(self):
        self._execute_query(ddl.CREATE_TABLES)

    def drop_tables(self):
        self._execute_query(ddl.DROP_TABLES)

    def fill_authors(self, authors):
        attrs = [{'name': author} for author in authors]
        self._execute_query(dml.INSERT_AUTHORS, params=attrs)

    def fill_products(self, products):
        attrs = [{'name': product} for product in products]
        self._execute_query(dml.INSERT_PRODUCTS, params=attrs)

    def fill_shops(self, shops):
        shop_attrs = [{'name': shop['name']} for shop in shops]

        with self.engine.connect() as conn:
            conn.execute(text(dml.INSERT_SHOPS), shop_attrs)

            for shop in shops:
                shop_products_attrs = [
                    {
                        'prod_name': prod['prod_name'],
                        'shop_name': shop['name'],
                        'price': prod['price']
                    } for prod in shop['products']
                ]
                conn.execute(
                    text(dml.INSERT_SHOP_PRODUCTS), shop_products_attrs)

    def fill_recipes(self, recipes):
        with self.engine.connect() as conn:
            for recipe in recipes:
                # insert recipe
                recipe_attrs = {
                    'title': recipe['title'],
                    'text': recipe['text'],
                    'portions': recipe['portions'],
                    'author_name': recipe['author']
                }
                conn.execute(text(dml.INSERT_RECIPE), recipe_attrs)
                # insert recipe's tags
                recipe_tags_attrs = [{
                    'title': recipe['title'],
                    'tag_name': tag
                } for tag in recipe['tags']]
                conn.execute(text(dml.INSERT_RECIPE_TAGS), recipe_tags_attrs)
                recipe_products_attrs = [
                    {
                        'title': recipe['title'],
                        'name': prod['product'],
                        'weight': prod['weight']
                    } for prod in recipe['products']
                ]
                conn.execute(
                    text(dml.INSERT_RECIPE_PRODUCTS), recipe_products_attrs
                )

    def _execute_query(
            self, query: str, params: Optional[list] = None) -> CursorResult:

        with self.engine.connect() as conn:
            res = conn.execute(text(query), params)

        return res

    def _create_engine(self) -> sqlalchemy.engine.Engine:
        return create_engine(self._get_db_url())

    def _get_db_url(self) -> str:
        return os.path.join(self.db_url, self.db_name)
