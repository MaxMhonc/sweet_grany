import os

import sqlalchemy
from sqlalchemy import create_engine, insert, select, bindparam

from sweet_grany_app.service_abstract import AbstractService
from sweet_grany_app.models.core_models import (
    meta_object,
    authors as authors_table,
    tags as tags_table,
    products as products_table,
    shops as shops_table,
    products_shop as products_shops_table,
    recipes as recipes_table,
    tags_recipes as tags_recipes_table,
    products_recipe as products_recipe_table
)


class CoreService(AbstractService):

    def __init__(self, db_url: str, db_name: str,
                 meta_object: sqlalchemy.MetaData):
        self.db_url = db_url
        self.db_name = db_name
        self.meta_object = meta_object
        self.engine = self._create_engine()
        self._bind_metaobject()

    @classmethod
    def tell_type(cls):
        pass

    def create_all_tables(self):
        self.meta_object.create_all()

    def drop_all_tables(self):
        self.meta_object.drop_all()

    def fill_in_authors(self, authors):
        attrs = [{'name': author} for author in authors]
        with self.engine.connect() as conn:
            conn.execute(insert(authors_table), attrs)

    def fill_in_tags(self, tags):
        attrs = [{'name': tag} for tag in tags]
        with self.engine.connect() as conn:
            conn.execute(insert(tags_table), attrs)

    def fill_in_products(self, products):
        attrs = [{'name': product} for product in products]
        with self.engine.connect() as conn:
            conn.execute(insert(products_table), attrs)

    def fill_in_shops(self, shops):
        shop_attrs = [{'name': shop['name']} for shop in shops]
        with self.engine.connect() as conn:
            conn.execute(insert(shops_table), shop_attrs)
            for shop in shops:
                prod_id = select(products_table.c.product_id).where(
                    products_table.c.name == bindparam('prod_name')
                ).scalar_subquery()
                shop_id = select(shops_table.c.shop_id).where(
                    shops_table.c.name == bindparam('shop_name')
                ).scalar_subquery()
                shop_products_attrs = [
                    {
                        'prod_name': prod['prod_name'],
                        'shop_name': shop['name'],
                        'whole': prod['price'].split('.')[0],
                        'decimal': prod['price'].split('.')[1]
                    } for prod in shop['products']
                ]
                insert_command = products_shops_table.insert({
                    'product_id': prod_id,
                    'shop_id': shop_id,
                    'price_whole_part': bindparam("whole"),
                    'price_decimal_part': bindparam("decimal")
                })
                conn.execute(insert_command, shop_products_attrs)

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
                author_id = select(authors_table.c.author_id).where(
                    authors_table.c.name == bindparam('author_name')
                ).scalar_subquery()
                insert_command = recipes_table.insert({
                    'title': bindparam('title'),
                    'text': bindparam('text'),
                    'portions': bindparam('portions'),
                    'author_id': author_id
                })
                conn.execute(insert_command, recipe_attrs)
                # insert recipe's tags
                recipe_tags_attrs = [{
                    'title': recipe['title'],
                    'tag_name': tag
                } for tag in recipe['tags']]
                recipe_id = select(recipes_table.c.recipe_id).where(
                    recipes_table.c.title == bindparam('title')
                ).scalar_subquery()
                tag_id = select(tags_table.c.tag_id).where(
                    tags_table.c.name == bindparam('tag_name')
                ).scalar_subquery()
                insert_command = tags_recipes_table.insert({
                    'recipe_id': recipe_id,
                    'tag_id': tag_id
                })
                conn.execute(insert_command, recipe_tags_attrs)
                # insert recipe's prods
                recipe_products_attrs = [
                    {
                        'title': recipe['title'],
                        'name': prod['product'],
                        'whole': prod['weight'].split('.')[0],
                        'decimal': prod['weight'].split('.')[1]
                    } for prod in recipe['products']]
                product_id = select(products_table.c.product_id).where(
                    products_table.c.name == bindparam('name')
                ).scalar_subquery()
                insert_command = products_recipe_table.insert({
                    'recipe_id': recipe_id,
                    'product_id': product_id,
                    'amount_whole_part': bindparam('whole'),
                    'amount_decimal_part': bindparam('decimal')
                })
                conn.execute(insert_command, recipe_products_attrs)

    def _create_engine(self) -> sqlalchemy.engine.Engine:
        return create_engine(self._get_db_url())

    def _get_db_url(self) -> str:
        return os.path.join(self.db_url, self.db_name)

    def _bind_metaobject(self):
        self.meta_object.bind = self.engine


if __name__ == '__main__':
    url = "postgresql://localhost:5432/"
    name = 'sweet_granny_test'
    worker = CoreService(url, name, meta_object)
    # worker.drop_all_tables()

    worker.create_all_tables()
    worker.fill_in_authors(['max', 'bob'])
