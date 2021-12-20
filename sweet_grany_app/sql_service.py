import os

import sqlalchemy.engine
from sqlalchemy import create_engine, text

from sweet_grany_app.abstract_service import AbstractService


class SQLService(AbstractService):

    def __init__(self, db_uri: str, db_name: str, query_path: str):
        self.query_path = query_path
        self.db_uri = db_uri
        self.db_name = db_name
        self.engine = self._create_engine()

    @classmethod
    def tell_type(cls):
        return 'core'

    def create_all_tables(self):
        with self.engine.connect() as conn:
            conn.execute(text(self._read_query('create_all_tables.sql')))

    def drop_all_tables(self):
        with self.engine.connect() as conn:
            conn.execute(text(self._read_query('drop_all_tables.sql')))

    def fill_in_authors(self, authors):
        attrs = [{'name': author} for author in authors]
        with self.engine.connect() as conn:
            conn.execute(
                text('INSERT INTO authors (name) VALUES (:name);'),
                attrs
            )

    def fill_in_products(self, products):
        attrs = [{'name': product} for product in products]
        with self.engine.connect() as conn:
            conn.execute(
                text('INSERT INTO products (name) VALUES (:name);'),
                attrs
            )

    def fill_in_shops(self, shops):
        shop_attrs = [{'name': shop['name']} for shop in shops]
        with self.engine.connect() as conn:
            conn.execute(
                text('INSERT INTO shops (name) VALUES (:name);'),
                shop_attrs
            )
            for shop in shops:
                shop_products_attrs = [
                    {
                        'prod_name': prod['prod_name'],
                        'shop_name': shop['name'],
                        'price': prod['price']
                    } for prod in shop['products']
                ]
                conn.execute(
                    text("""
            INSERT INTO products_shop
            (product_id, shop_id, price)
            VALUES ((SELECT id FROM products WHERE name = :prod_name),
            (SELECT id FROM shops WHERE name = :shop_name),
            :price);
                    """),
                    shop_products_attrs
                )

    def fill_in_recipes(self, recipes):
        with self.engine.connect() as conn:
            for recipe in recipes:
                # insert recipe
                recipe_attrs = {
                    'title': recipe['title'],
                    'text': recipe['text'],
                    'portions': recipe['portions'],
                    'author_name': recipe['author']
                }
                conn.execute(
                    text("""
                    INSERT INTO recipes (title, text, portions, author_id)
                    VALUES (:title, :text, :portinos,
                    (SELECT id FROM authors WHERE name = :author_name));
                    """), recipe_attrs
                )
                # insert recipe's tags
                recipe_tags_attrs = [{
                    'title': recipe['title'],
                    'tag_name': tag
                } for tag in recipe['tags']]
                conn.execute(
                    text(
                        """
                        INSERT INTO tags (name, recipe_id)
                        VALUES (:tag_name,
                        (SELECT id FROM recipes WHERE title = :title));
                        """
                    ), recipe_tags_attrs
                )
                recipe_products_attrs = [
                    {
                        'title': recipe['title'],
                        'name': prod['product'],
                        'weight': prod['weight']
                    } for prod in recipe['products']
                ]
                conn.execute(
                    text("""
                    INSERT INTO products_recipe
                    (recipe_id, product_id, weight)
                    VALUES (
                    (SELECT id FROM recipes WHERE title = :title),
                    (SELECT id FROM products WHERE name = :name),
                    :weight);"""), recipe_products_attrs
                )

    def _read_query(self, file_name: str) -> str:
        with open(os.path.join(
                self.query_path, file_name), 'r') as file:
            query = file.read()
        return query

    def _create_engine(self) -> sqlalchemy.engine.Engine:
        return create_engine(self._get_db_url())

    def _get_db_url(self) -> str:
        return os.path.join(self.db_uri, self.db_name)
