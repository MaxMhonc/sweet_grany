from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (Column, Integer, Text, SmallInteger, NUMERIC,
                        VARCHAR, ForeignKey, CheckConstraint)

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False, unique=True)

    recipes = relationship('Recipe', back_populates='author')

    def __repr__(self):
        return f'Author {self.id} - {self.name}'


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False)
    recipe_id = Column(Integer(), ForeignKey('recipes.id', ondelete='CASCADE'))

    recipes = relationship('Recipe', back_populates='tags')

    def __repr__(self):
        return f'Tag {self.id} - {self.name}'


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(VARCHAR(length=200), nullable=False)
    text = Column(Text(), nullable=False)
    portions = Column(SmallInteger(), CheckConstraint('portions>0'))
    author_id = Column(
        Integer(), ForeignKey('authors.id', ondelete='SET NULL')
    )

    author = relationship('Author', back_populates='recipes')
    products = relationship('ProductRecipe', back_populates='recipes')
    tags = relationship('Tag', back_populates='recipes')

    def __repr__(self):
        return f'Recipe {self.id} - {self.title}'


class ProductRecipe(Base):
    __tablename__ = 'products_recipe'

    recipe_id = Column(
        Integer(), ForeignKey('recipes.id', ondelete='CASCADE'),
        primary_key=True)
    product_id = Column(
        Integer(), ForeignKey('products.id', ondelete='CASCADE'),
        primary_key=True)
    weight = Column(
        NUMERIC(), CheckConstraint('weight>0'), nullable=False
    )

    products = relationship("Product", back_populates="recipes")
    recipes = relationship("Recipe", back_populates="products")

    def __repr__(self):
        return (f'Prod-{self.product_id} for Recipe-{self.recipe_id=} '
                f'with {self.weight=}')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False)

    recipes = relationship('ProductRecipe', back_populates='products')
    shops = relationship('ProductsShop', back_populates='products')

    def __repr__(self):
        return f'Product {self.id} - {self.name}'


class ProductsShop(Base):
    __tablename__ = 'products_shop'

    product_id = Column(
        Integer(), ForeignKey('products.id', ondelete='CASCADE'),
        primary_key=True)
    shop_id = Column(
        Integer(), ForeignKey('shops.id', ondelete='CASCADE'),
        primary_key=True)
    price = Column(NUMERIC(), CheckConstraint('price>0'), nullable=False)

    products = relationship("Product", back_populates="shops")
    shops = relationship("Shop", back_populates="products")

    def __repr__(self):
        return (f'Product {self.product_id} for Shop {self.shop_id}'
                f'with {self.price=}')

    def __lt__(self, other):
        return self.price < other.price


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=100), nullable=False)

    products = relationship('ProductsShop', back_populates='shops')

    def __repr__(self):
        return f'Shop {self.id} - {self.name}'
