from abc import ABC, abstractmethod


class AbstractService(ABC):

    @classmethod
    @abstractmethod
    def tell_type(cls):
        pass

    @abstractmethod
    def create_all_tables(self):
        pass

    @abstractmethod
    def drop_all_tables(self):
        pass

    @abstractmethod
    def fill_in_authors(self, authors):
        pass

    @abstractmethod
    def fill_in_products(self, products):
        pass

    @abstractmethod
    def fill_in_shops(self, shops):
        pass

    @abstractmethod
    def fill_in_recipes(self, recipes):
        pass
