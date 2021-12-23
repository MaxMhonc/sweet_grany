from typing import List, Dict


class DataGenerator:

    def __init__(
            self,
            tags_manager,
            authors_manager,
            products_manager,
            shop_manager,
            recipe_manager
    ):
        self.tags_manager = tags_manager
        self.authors_manager = authors_manager
        self.products_manager = products_manager
        self.shop_manager = shop_manager
        self.recipe_manager = recipe_manager

    def generate_tags(self) -> List[str]:
        """
        Generate list of tags
        :return: ['tag1', 'tag2', ...]
        """
        tags = self.tags_manager.get_all_tags()
        return tags

    def generate_authors(self) -> List[str]:
        """
        Generate list of authors
        :return: ['author1', 'author2', ...]
        """
        author_names = self.authors_manager.get_all_authors()
        return author_names

    def generate_products(self) -> List[str]:
        """Generate list of product names"""
        products = self.products_manager.get_all_products_names()
        return products

    def generate_shops(self) -> List[Dict[str, object]]:
        shop_info = self.shop_manager.get_shops_data()
        return shop_info

    def generate_recipe(self) -> Dict[str, object]:
        recipe = {
            'title': self.recipe_manager.get_title(),
            'author': self.authors_manager.get_random_author(),
            'tags': self.tags_manager.get_tags_set(),
            'text': self.recipe_manager.get_text(),
            'portions': self.recipe_manager.get_portions(),
            'products': self.recipe_manager.get_products_weight()
        }
        return recipe

    def generate_recipes(self, amount: int):
        recipes = [self.generate_recipe() for _ in range(amount)]
        return self._remove_repeating(recipes)

    @staticmethod
    def _remove_repeating(sequence):
        sub_sequence = {}
        for item in sequence:
            sub_sequence[item['title']] = item
        return list(sub_sequence.values())
