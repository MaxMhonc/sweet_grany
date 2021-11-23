from random import randint, sample
from typing import List, Tuple


class Products:
    """
    Product instance generate list of products from self.products_list,
    containing random number of prods between self.prod_min and self.prod_max.
    Each product is in tuple with its weight up to self.max_weight with
    self.decimal_places digits after coma.
    """

    def __init__(
            self,
            products_list: list,
            prod_min: int = 3,
            prod_max: int = 5,
            max_weight: int = 3,  # 5 > max_weight >= 1
            decimal_places: int = 2  # 3 > decimal_places >= 1
    ):
        self.products_list = products_list
        self.prod_min = min(abs(prod_min), abs(prod_max))
        self.prod_max = max(abs(prod_min), abs(prod_max))
        self.max_weight = max_weight if 5 >= max_weight >= 1 else 1
        self.decimal_places = decimal_places if 3 >= decimal_places >= 1 else 2

    def generate_products(self) -> List[Tuple[str, str]]:
        """Returns list of tuples (product name, weight)"""
        return [(prod, self._get_prod_weight())
                for prod in self._get_product_slice()]

    def _get_prod_weight(self) -> str:
        whole_weight = randint(0, self.max_weight - 1)
        decimal_weight = randint(1, 10 * self.decimal_places)
        template = '{}.{:0' + str(self.decimal_places) + '}'
        return template.format(whole_weight, decimal_weight)

    def _get_product_slice(self) -> List[str]:
        return sample(self.products_list, self._get_prods_amount())

    def _get_prods_amount(self) -> int:
        return randint(self.prod_min, self.prod_max)
