from . import sql_queries
from .db_handler import DBHandler


def create_all_tables(db_name: str):
    handler = DBHandler(db_name)
    handler.execute_query(sql_queries.CREATE_ALL_TABLES)


def drop_all_tables(db_name: str):
    handler = DBHandler(db_name)
    handler.execute_query(sql_queries.DROP_ALL_TABLES)


if __name__ == '__main__':
    db_name = 'sweet_granny'
    # create_all_tables(db_name)
    drop_all_tables(db_name)
