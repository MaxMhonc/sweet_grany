import os

from sweet_grany_app.data_service.db_handler_psycopg import DBHandler
from sweet_grany_app.abstract_service import AbstractService


class PsycopgService(AbstractService):

    def __init__(self, path, db_name: str = 'sweet_granny'):
        self.query_directory_path = path
        self.handler = DBHandler(db_name)

    @classmethod
    def tell_type(cls):
        return 'sql'

    def create_all_tables(self):
        self.handler.execute_query(self._read_query('create_all_tables.sql'))

    def drop_all_tables(self):
        self.handler.execute_query(self._read_query('drop_all_tables.sql'))

    def fill_in_authors(self, authors: list[str]):
        command = self._replace_placeholders(
            self._read_query('insert_author.sql'))
        with self.handler as cursor:
            for author in authors:
                cursor.execute(command, (author,))

    def fill_in_tags(self, tags: list[str]):
        command = self._replace_placeholders(
            self._read_query('insert_tag.sql'))
        with self.handler as cursor:
            for tag in tags:
                cursor.execute(command, (tag,))

    def fill_in_products(self, products: list[str]):
        command = self._replace_placeholders(
            self._read_query('insert_product.sql'))
        with self.handler as cursor:
            for product in products:
                cursor.execute(command, (product,))

    def fill_in_shops(self, shops: list[dict[str, list[dict[str, str]]]]):
        insert_shop_command = self._replace_placeholders(
            self._read_query('insert_shop.sql'))
        insert_product_command = self._replace_placeholders(
            self._read_query('insert_product_shop.sql'))
        for shop in shops:
            # insert shop info
            with self.handler as cursor:
                cursor.execute(insert_shop_command, (shop['name'],))
            # fill in shop's products data
            with self.handler as cursor:
                for prod in shop['products']:
                    prod_name = prod['prod_name']
                    whale_price, decimal_price = prod['price'].split('.')
                    cursor.execute(
                        insert_product_command,
                        (prod_name, shop['name'], whale_price, decimal_price)
                    )

    def fill_in_recipes(self, recipes):
        insert_recipe_command = self._replace_placeholders(
            self._read_query('insert_recipes.sql'))
        insert_tags_recipes_command = self._replace_placeholders(
            self._read_query('insert_tags_recipes.sql'))
        insert_products_recipe_command = self._replace_placeholders(
            self._read_query('insert_products_recipe.sql'))
        # insert recipe info
        for recipe in recipes:
            with self.handler as cursor:
                cursor.execute(
                    insert_recipe_command, (
                        recipe['title'],
                        recipe['text'],
                        recipe['portions'],
                        recipe['author']
                    ))
            # fill in recipe's tags info
            with self.handler as cursor:
                for tag in recipe['tags']:
                    cursor.execute(insert_tags_recipes_command, (
                        recipe['title'],
                        tag
                    ))
            # fill in recipe's products info
            with self.handler as cursor:
                for product in recipe['products']:
                    whale, decimal = product['weight'].split('.')
                    cursor.execute(
                        insert_products_recipe_command, (
                            recipe['title'],
                            product['product'],
                            whale,
                            decimal
                        ))

    def _read_query(self, file_name: str) -> str:
        with open(os.path.join(
                self.query_directory_path, file_name), 'r') as file:
            query = file.read()
        return query

    @staticmethod
    def _replace_placeholders(query: str) -> str:
        return query.replace("'<plaseholder>'", '%s')


if __name__ == '__main__':
    # db_name = 'sweet_granny'
    path = os.path.join(os.getcwd(), 'data_service', 'sql_queries')
    sql_service = PsycopgService(path)
    # sql_service.create_all_tables()
    sql_service.drop_all_tables()
