import os

import sqlalchemy.engine
from sqlalchemy import create_engine, text

from sweet_grany_app.service_abstract import AbstractService


class CoreService(AbstractService):

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

    def fill_in_tags(self, tags):
        attrs = [{'name': tag} for tag in tags]
        with self.engine.connect() as conn:
            conn.execute(
                text('INSERT INTO tags (name) VALUES (:name);'),
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
                        'whole': prod['price'].split('.')[0],
                        'decimal': prod['price'].split('.')[1]
                    } for prod in shop['products']
                ]
                conn.execute(
                    text("""
            INSERT INTO products_shop 
            (product_id, shop_id, price_whole_part, price_decimal_part)
            VALUES ((SELECT product_id FROM products WHERE name = :prod_name),
            (SELECT shop_id FROM shops WHERE name = :shop_name),
            :whole, :decimal);
                    """),
                    shop_products_attrs
                )

    def fill_in_recipes(self, recipes):
        with self.engine.connect() as conn:
            for recipe in recipes:
                recipe_attrs = {
                    'title': recipe['title'],
                    'text': recipe['text'],
                    'portinos': recipe['portions'],
                    'author_name': recipe['author']
                }
                conn.execute(
                    text("""
                    INSERT INTO recipes (title, text, portions, author_id)
                    VALUES (:title, :text, :portinos,
                    (SELECT author_id FROM authors WHERE name = :author_name));
                    """), recipe_attrs
                )
                recipe_tags_attrs = [{
                    'title': recipe['title'],
                    'tag_name': tag
                } for tag in recipe['tags']]
                conn.execute(
                    text("""
                    INSERT INTO tags_recipes (recipe_id, tag_id)
                    VALUES (
                    (SELECT recipe_id FROM recipes WHERE title = :title),
                    (SELECT tag_id FROM tags WHERE name = :tag_name));
                    """), recipe_tags_attrs
                )
                recipe_products_attrs = [
                    {
                        'title': recipe['title'],
                        'name': prod['product'],
                        'whole': prod['weight'].split('.')[0],
                        'decimal': prod['weight'].split('.')[1]
                    } for prod in recipe['products']
                ]
                conn.execute(
                    text("""
                    INSERT INTO products_recipe 
                    (recipe_id, product_id, amount_whole_part, 
                    amount_decimal_part)
                    VALUES (
                    (SELECT recipe_id FROM recipes WHERE title = :title),
                    (SELECT product_id FROM products WHERE name = :name),
                    :whole, :decimal);"""), recipe_products_attrs
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


if __name__ == '__main__':
    worker = CoreService(
        'postgresql://localhost:5432',
        'sweet_granny_test',
        os.path.join(os.getcwd(), 'data_service', 'sql_queries')
    )
    # worker.create_all_tables()
    worker.drop_all_tables()
