from typing import Optional

import psycopg2


class DBHandler:

    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query: str, params: Optional[tuple[str]] = None):
        with psycopg2.connect(self._concat_dsn()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
        return cursor

    def _concat_dsn(self) -> str:
        dsn = f'dbname={self.db_name}'
        return dsn

    def __enter__(self):
        self.connection = psycopg2.connect(self._concat_dsn())
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_val:
            raise exc_type(exc_val)
