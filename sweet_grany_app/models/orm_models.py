from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (Table, Column,
                        INTEGER, VARCHAR, TEXT, SMALLINT, ForeignKey,
                        CheckConstraint)

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False)

    recipes = relationship('Recipe', back_populates='author')

    def __repr__(self):
        return f'Author {self.author_id} - {self.name}'


class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False)

    recipes = relationship('Recipe', secondary='tags_recipes',
                           back_populates='tags')

    def __repr__(self):
        return f'Tag {self.tag_id} - {self.name}'


tags_recipes = Table(
    'tags_recipes',
    Base.metadata,
    Column('recipe_id', INTEGER(),
           ForeignKey('recipes.recipe_id', ondelete='CASCADE'),
           primary_key=True),
    Column('tag_id', INTEGER(),
           ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True)
)


class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    title = Column(VARCHAR(length=200), nullable=False)
    text = Column(TEXT(), nullable=False)
    portions = Column(SMALLINT(), CheckConstraint('portions>0'))
    author_id = Column(
        INTEGER(), ForeignKey('authors.author_id', ondelete='SET NULL')
    )

    author = relationship('Author', back_populates='recipes')
    products = relationship('ProductRecipe', back_populates='recipes')
    tags = relationship('Tag', secondary='tags_recipes',
                        back_populates='recipes')

    def __repr__(self):
        return f'Recipe {self.recipe_id} - {self.title}'


class ProductRecipe(Base):
    __tablename__ = 'products_recipe'

    recipe_id = Column(
        INTEGER(), ForeignKey('recipes.recipe_id', ondelete='CASCADE'),
        primary_key=True)
    product_id = Column(
        INTEGER(), ForeignKey('products.product_id', ondelete='CASCADE'),
        primary_key=True)
    amount_whole_part = Column(
        INTEGER(), CheckConstraint('amount_whole_part>=0'), nullable=False)
    amount_decimal_part = Column(
        INTEGER(), CheckConstraint('amount_decimal_part>=0'))

    products = relationship("Product", back_populates="recipes")
    recipes = relationship("Recipe", back_populates="products")

    def __repr__(self):
        return (f'Prod-{self.product_id} for Recipe-{self.recipe_id} '
                f'with {self.amount_whole_part}.{self.amount_decimal_part}')


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False)

    recipes = relationship('ProductRecipe', back_populates='products')
    shops = relationship('ProductsShop', back_populates='products')

    def __repr__(self):
        return f'Product {self.product_id} - {self.name}'


class ProductsShop(Base):
    __tablename__ = 'products_shop'

    product_id = Column(
        INTEGER(), ForeignKey('products.product_id', ondelete='CASCADE'),
        primary_key=True)
    shop_id = Column(
        INTEGER(), ForeignKey('shops.shop_id', ondelete='CASCADE'),
        primary_key=True)
    price_whole_part = Column(
        INTEGER(), CheckConstraint('price_whole_part>=0'), nullable=False)
    price_decimal_part = Column(
        INTEGER(), CheckConstraint('price_decimal_part>=0'))

    products = relationship("Product", back_populates="shops")
    shops = relationship("Shop", back_populates="products")

    def __repr__(self):
        return (f'Product {self.product_id} for Shop {self.shop_id}'
                f'with {self.price_whole_part}.{self.price_decimal_part}')


class Shop(Base):
    __tablename__ = 'shops'

    shop_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False)

    products = relationship('ProductsShop', back_populates='shops')

    def __repr__(self):
        return f'Shop {self.shop_id} - {self.name}'
