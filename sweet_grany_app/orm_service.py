import os

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from sweet_grany_app.abstract_service import AbstractService
from sweet_grany_app.models.orm_models import (
    Author, Tag, Product, Shop, ProductsShop, Recipe, ProductRecipe)


class ORMService(AbstractService):

    def __init__(self, db_url: str, db_name: str, base):
        self.db_url = db_url
        self.db_name = db_name
        self.base = base
        self.engine = self._create_engine()
        self.session = Session(self.engine)

    @classmethod
    def tell_type(cls):
        pass

    def create_all_tables(self):
        self.base.metadata.create_all(self.engine)

    def drop_all_tables(self):
        self.base.metadata.drop_all(self.engine)

    def fill_in_authors(self, authors):
        author_instances = [Author(name=author) for author in authors]
        self.session.add_all(author_instances)
        self.session.commit()

    def fill_in_tags(self, tags):
        tag_instances = [Tag(name=tag) for tag in tags]
        self.session.add_all(tag_instances)
        self.session.commit()

    def fill_in_products(self, products):
        prod_instances = [Product(name=prod) for prod in products]
        self.session.add_all(prod_instances)
        self.session.commit()

    def fill_in_shops(self, shops):
        for shop in shops:
            shop_to_db = Shop(name=shop['name'])
            with self.session.no_autoflush as s:
                for prod in shop['products']:
                    product = s.execute(select(Product).where(
                        Product.name == prod['prod_name']
                    )).scalar()
                    shop_prod = ProductsShop(
                        price_whole_part=prod['price'].split('.')[0],
                        price_decimal_part=prod['price'].split('.')[1]
                    )
                    shop_to_db.products.append(shop_prod)
                    product.shops.append(shop_prod)
                    s.add(shop_prod)
            self.session.commit()

    def fill_in_recipes(self, recipes):
        for recipe in recipes:
            rec = Recipe(
                title=recipe['title'],
                text=recipe['text'],
                portions=recipe['portions']
            )
            with self.session.no_autoflush as s:
                author = s.execute(
                    select(Author).where(
                        Author.name == recipe['author'])).scalar()
                author.recipes.append(rec)
                for tag in recipe['tags']:
                    recipe_tag = s.execute(select(Tag).where(
                        Tag.name == tag)).scalar()
                    rec.tags.append(recipe_tag)
                for prod in recipe['products']:
                    product = s.execute(
                        select(Product).where(
                            Product.name == prod['product'])).scalar()
                    prod_rec = ProductRecipe(
                        amount_whole_part=prod['weight'].split('.')[0],
                        amount_decimal_part=prod['weight'].split('.')[1]
                    )
                    product.recipes.append(prod_rec)
                    rec.products.append(prod_rec)
                    s.add(prod_rec)
            self.session.commit()

    def _create_engine(self) -> sqlalchemy.engine.Engine:
        return create_engine(self._get_db_url())

    def _get_db_url(self) -> str:
        return os.path.join(self.db_url, self.db_name)
