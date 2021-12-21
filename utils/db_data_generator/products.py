from typing import List


class Products:
    """
    Product instance generate list of products from 'products_list'.
    """

    def __init__(
            self,
            products_list: list,
    ):
        self.products_list = products_list

    def get_all_products_names(self) -> List[str]:
        """Returns list of all available product names"""
        return self.products_list
