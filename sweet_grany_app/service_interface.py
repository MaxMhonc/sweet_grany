from abc import ABC, abstractmethod


class AbstractService(ABC):
    """Main interface for interaction with DB tables.
    Look DB diagram in "documentation" folder"""

    @abstractmethod
    def create_tables(self):
        """Creates all tables for DB."""

    @abstractmethod
    def drop_tables(self):
        """Drops all ables from DB."""

    @abstractmethod
    def fill_authors(self, authors: list):
        """Takes authors info and inserts into table(s)"""

    @abstractmethod
    def fill_products(self, products: list):
        """Takes products info and inserts into table(s)"""

    @abstractmethod
    def fill_shops(self, shops: list):
        """Takes shops info and inserts into table(s)"""

    @abstractmethod
    def fill_recipes(self, recipes: list):
        """Takes recipes info and inserts into table(s)"""

    @abstractmethod
    def get_recipe_costs(self, title: str):
        """Returns max and min cost for recipe by its title"""

    @abstractmethod
    def get_components_price(self, title: str):
        """Returns cheaper prices for recipe's components"""
