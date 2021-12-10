from sqlalchemy import (create_engine, Table, MetaData, Column,
                        INTEGER, VARCHAR, TEXT, SMALLINT, ForeignKey,
                        CheckConstraint)

# engine = create_engine("postgresql://localhost:5432/sweet_granny",
#                        echo=True, future=True)


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
    Column('author_id', INTEGER(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False)
)
recipes = Table(
    'recipes',
    meta_object,
    Column('recipe_id', INTEGER(), primary_key=True, autoincrement=True),
    Column('title', VARCHAR(length=200), nullable=False),
    Column('text', TEXT(), nullable=False),
    Column('portions', SMALLINT(), CheckConstraint('portions>0')),
    Column('author_id', INTEGER(), ForeignKey(
        'authors.author_id', ondelete='SET NULL'))
)
products_shop = Table(
    'products_shop',
    meta_object,
    Column('product_id', INTEGER(), ForeignKey('products.product_id',
                                               ondelete='CASCADE')),
    Column('shop_id', INTEGER(), ForeignKey('shops.shop_id',
                                            ondelete='CASCADE')),
    Column(
        'price_whole_part', INTEGER(),
        CheckConstraint('price_whole_part>=0'),
        nullable=False
    ),
    Column(
        'price_decimal_part',
        INTEGER(),
        CheckConstraint('price_decimal_part>=0')
    )
)
shops = Table(
    'shops',
    meta_object,
    Column('shop_id', INTEGER(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False)
)
tags_recipes = Table(
    'tags_recipes',
    meta_object,
    Column('recipe_id', INTEGER(), ForeignKey('recipes.recipe_id',
                                              ondelete='CASCADE')),
    Column('tag_id', INTEGER(), ForeignKey('tags.tag_id',
                                           ondelete='CASCADE'))
)
tags = Table(
    'tags',
    meta_object,
    Column('tag_id', INTEGER(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False)
)
products_recipe = Table(
    'products_recipe',
    meta_object,
    Column('recipe_id', INTEGER(), ForeignKey('recipes.recipe_id',
                                              ondelete='CASCADE')),
    Column('product_id', INTEGER(), ForeignKey('products.product_id',
                                               ondelete='CASCADE')),
    Column('amount_whole_part', INTEGER(),
           CheckConstraint('amount_whole_part>=0'), nullable=False),
    Column('amount_decimal_part', INTEGER(),
           CheckConstraint('amount_decimal_part>=0'))
)
products = Table(
    'products',
    meta_object,
    Column('product_id', INTEGER(), primary_key=True, autoincrement=True),
    Column('name', VARCHAR(length=100), nullable=False)
)

if __name__ == '__main__':
    get_tables_schemas("postgresql://localhost:5432/sweet_granny")
