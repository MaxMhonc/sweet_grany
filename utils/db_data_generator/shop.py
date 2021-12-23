from typing import List, Dict, Union
from random import sample, randint, shuffle

ProductsPriceList = List[Dict[str, str]]
ShopTypeModel = dict[str, Union[str, list[dict[str, str]]]]


class Shop:
    """
    Shop instance is initialised with shop names list and products list.
    Via get_shop_data_generator it returns shop name form 'shop_names'
    with product list that is 'prod_percent' percent long of 'products'.
    Prise in range from 'min_price' to 'max_price' corresponds to each
    shop product.
    Iteration number is equal to shop names amount.
    """

    def __init__(
            self,
            shop_names: List[str],
            products: List[str],
            prod_percent: int = 75,
            min_price: int = 10,
            max_price: int = 500
    ):
        self.shop_names = shop_names
        self._shuffle_names()
        self.prods = products
        self.prod_percent = prod_percent
        self.min_price = min_price
        self.max_price = max_price

    def get_all_shops(self):
        return self.shop_names

    def get_shops_data(self) -> list[ShopTypeModel]:
        """
        Generate shop info in format:
        {
          'name': <shop name>,
          'products': [
            {
              'prod_name': <prod_name>,
              'price': <product price>
            }
          ]
        }
        """
        return [{
            'name': name,
            'products': self._get_prods_price_list()
        } for name in self.shop_names]

    def _get_shop_products(self) -> List[str]:
        total_amount = int((len(self.prods) / 100) * self.prod_percent)
        return sample(self.prods, total_amount)

    def _generate_price(self) -> str:
        whole_price = randint(self.min_price, self.max_price - 1)
        decimal_price = randint(1, 99)
        return '{}.{:02}'.format(whole_price, decimal_price)

    def _get_prods_price_list(self) -> ProductsPriceList:
        return [
            {
                'prod_name': prod_name,
                'price': self._generate_price()
            } for prod_name in self._get_shop_products()
        ]

    def _shuffle_names(self):
        shuffle(self.shop_names)
