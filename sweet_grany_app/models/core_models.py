from sqlalchemy import (create_engine, Table, MetaData, Column,
                        Integer, Text, SmallInteger, NUMERIC,
                        VARCHAR, ForeignKey,
                        CheckConstraint)


def get_tables_schemas(url):
    """Little chit to get db tables info if they are created"""
    engine = create_engine(url)
    tables = engine.table_names()
    print(tables)
    for table in tables:
        print(Table(table, MetaData(), autoload_with=engine).__repr__())


meta_object = MetaData()

authors = Table(
    'authors',
    meta_object,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False, unique=True)
)

recipes = Table(
    'recipes',
    meta_object,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('title', VARCHAR(length=200), nullable=False, unique=True),
    Column('text', Text(), nullable=False),
    Column('portions', SmallInteger(), CheckConstraint('portions>0')),
    Column('author_id', Integer(), ForeignKey(
        'authors.id', ondelete='SET NULL'))
)

products_shop = Table(
    'products_shop',
    meta_object,
    Column('product_id', Integer(), ForeignKey('products.id',
                                               ondelete='CASCADE')),
    Column('shop_id', Integer(), ForeignKey('shops.id',
                                            ondelete='CASCADE')),
    Column(
        'price', NUMERIC(), CheckConstraint('price>0'), nullable=False
    )
)

shops = Table(
    'shops',
    meta_object,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False, unique=True)
)

tags = Table(
    'tags',
    meta_object,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False),
    Column(
        'recipe_id', Integer(), ForeignKey('recipes.id', ondelete='CASCADE')
    )
)

products_recipe = Table(
    'products_recipe',
    meta_object,
    Column('recipe_id', Integer(), ForeignKey('recipes.id',
                                              ondelete='CASCADE')),
    Column('product_id', Integer(), ForeignKey('products.id',
                                               ondelete='CASCADE')),
    Column('weight', NUMERIC(), CheckConstraint('weight>0'), nullable=False)
)

products = Table(
    'products',
    meta_object,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False)
)
