import os

import sqlalchemy
from sqlalchemy import create_engine, insert, select, bindparam, func, and_

from sweet_grany_app.service_interface import AbstractService
from sweet_grany_app.models.core_models import (
    authors as authors_tbl,
    tags as tags_tbl,
    products as prods_tbl,
    shops as shops_tbl,
    products_shop as prods_shops_tbl,
    recipes as recs_tbl,
    products_recipe as prods_rec_tbl
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

    def create_tables(self):
        self.meta_object.create_all()

    def drop_tables(self):
        self.meta_object.drop_all()

    def fill_authors(self, authors):
        attrs = [{'name': author} for author in authors]
        with self.engine.connect() as conn:
            conn.execute(insert(authors_tbl), attrs)

    def fill_in_tags(self, tags):
        attrs = [{'name': tag} for tag in tags]
        with self.engine.connect() as conn:
            conn.execute(insert(tags_tbl), attrs)

    def fill_products(self, products):
        attrs = [{'name': product} for product in products]
        with self.engine.connect() as conn:
            conn.execute(insert(prods_tbl), attrs)

    def fill_shops(self, shops):
        shop_attrs = [{'name': shop['name']} for shop in shops]
        with self.engine.connect() as conn:
            conn.execute(insert(shops_tbl), shop_attrs)
            for shop in shops:
                prod_id = select(prods_tbl.c.id).where(
                    prods_tbl.c.name == bindparam('prod_name')
                ).scalar_subquery()
                shop_id = select(shops_tbl.c.id).where(
                    shops_tbl.c.name == bindparam('shop_name')
                ).scalar_subquery()
                shop_products_attrs = [
                    {
                        'prod_name': prod['prod_name'],
                        'shop_name': shop['name'],
                        'price': prod['price']
                    } for prod in shop['products']
                ]
                insert_command = prods_shops_tbl.insert({
                    'product_id': prod_id,
                    'shop_id': shop_id,
                    'price': bindparam('price')
                })
                conn.execute(insert_command, shop_products_attrs)

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
                author_id = select(authors_tbl.c.id).where(
                    authors_tbl.c.name == bindparam('author_name')
                ).scalar_subquery()
                insert_command = recs_tbl.insert({
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
                recipe_id = select(recs_tbl.c.id).where(
                    recs_tbl.c.title == bindparam('title')
                ).scalar_subquery()
                insert_command = tags_tbl.insert({
                    'name': bindparam('tag_name'),
                    'recipe_id': recipe_id
                })
                conn.execute(insert_command, recipe_tags_attrs)

                # insert recipe's prods
                recipe_products_attrs = [
                    {
                        'title': recipe['title'],
                        'name': prod['product'],
                        'weight': prod['weight']
                    } for prod in recipe['products']]
                product_id = select(prods_tbl.c.id).where(
                    prods_tbl.c.name == bindparam('name')
                ).scalar_subquery()
                insert_command = prods_rec_tbl.insert({
                    'recipe_id': recipe_id,
                    'product_id': product_id,
                    'weight': bindparam('weight')
                })
                conn.execute(insert_command, recipe_products_attrs)

    def get_recipe_costs(self, title: str):
        attrs = {'title': title}

        recipe_id = select(
            recs_tbl.c.id
        ).where(
            recs_tbl.c.title == bindparam('title')
        ).scalar_subquery()

        recipe_prods_prices = (
            select(
                (prods_rec_tbl.c.weight *
                 func.max(prods_shops_tbl.c.price)).label(
                    'max_product_cost'),
                (prods_rec_tbl.c.weight *
                 func.min(prods_shops_tbl.c.price)).label(
                    'min_product_cost')
            ).select_from(
                prods_shops_tbl
            ).join(
                prods_tbl,
                prods_shops_tbl.c.product_id == prods_tbl.c.id
            ).join(
                prods_rec_tbl,
                prods_rec_tbl.c.product_id == prods_tbl.c.id
            ).where(
                prods_rec_tbl.c.recipe_id == recipe_id
            ).group_by(
                prods_tbl.c.id,
                prods_rec_tbl.c.weight
            )
        ).subquery()

        query = select(
            func.sum(recipe_prods_prices.c.max_product_cost),
            func.sum(recipe_prods_prices.c.min_product_cost)
        )

        with self.engine.connect() as conn:
            data = conn.execute(query, attrs)

        return data.fetchall()

    def get_components_price(self, title: str):
        attrs = {'title': title}

        recipe_id = select(
            recs_tbl.c.id
        ).where(
            recs_tbl.c.title == bindparam('title')
        ).scalar_subquery()

        prod_min_price = select(
            prods_shops_tbl.c.product_id,
            func.min(prods_shops_tbl.c.price).label('min_price')
        ).group_by(
            prods_shops_tbl.c.product_id
        ).subquery()

        prods_shops_min_price = select(
            prods_shops_tbl.c.product_id,
            prod_min_price.c.min_price,
            prods_shops_tbl.c.shop_id
        ).select_from(
            prods_shops_tbl
        ).join(
            prod_min_price,
            and_(
                prods_shops_tbl.c.product_id == prod_min_price.c.product_id,
                prods_shops_tbl.c.price == prod_min_price.c.min_price
            )
        ).subquery()

        query = select(
            prods_tbl.c.name,
            shops_tbl.c.name,
            prods_shops_min_price.c.min_price,
            prods_rec_tbl.c.weight,
            prods_rec_tbl.c.weight * prods_shops_min_price.c.min_price
        ).select_from(
            recs_tbl
        ).join(
            prods_rec_tbl,
            recs_tbl.c.id == prods_rec_tbl.c.recipe_id
        ).join(
            prods_tbl,
            prods_tbl.c.id == prods_rec_tbl.c.product_id
        ).join(
            prods_shops_min_price,
            prods_shops_min_price.c.product_id == prods_tbl.c.id
        ).join(
            shops_tbl,
            shops_tbl.c.id == prods_shops_min_price.c.shop_id
        ).where(
            prods_rec_tbl.c.recipe_id == recipe_id
        )

        with self.engine.connect() as conn:
            data = conn.execute(query, attrs)

        return data.fetchall()

    def _create_engine(self) -> sqlalchemy.engine.Engine:
        return create_engine(self._get_db_url())

    def _get_db_url(self) -> str:
        return os.path.join(self.db_url, self.db_name)

    def _bind_metaobject(self):
        self.meta_object.bind = self.engine
