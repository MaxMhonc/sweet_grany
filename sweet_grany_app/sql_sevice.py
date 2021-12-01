import os

from sweet_grany_app.data_service.db_handler import DBHandler


class SQLService:

    def __init__(self, path, db_name: str = 'sweet_granny'):
        self.query_directory_path = path
        self.handler = DBHandler(db_name)

    def read_query(self, file_name: str) -> str:
        with open(os.path.join(
                self.query_directory_path, file_name), 'r') as file:
            query = file.read()
        return query

    def create_all_tables(self):
        # handler = DBHandler(db_name)
        self.handler.execute_query(self.read_query('create_all_tables.sql'))

    def drop_all_tables(self):
        # handler = DBHandler(db_name)
        self.handler.execute_query(self.read_query('drop_all_tables.sql'))

    def fill_in_authors(self, authors: list[str]):
        command = 'INSERT INTO authors (name) VALUES (%s);'
        with self.handler as cursor:
            for author in authors:
                cursor.execute(command, (author,))


if __name__ == '__main__':
    # db_name = 'sweet_granny'
    path = os.path.join(os.getcwd(), 'data_service', 'sql_queries')
    sql_service = SQLService(path)
    # sql_service.create_all_tables()
    sql_service.drop_all_tables()
