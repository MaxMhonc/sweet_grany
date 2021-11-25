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
        """Generate list of tags"""
        tags = self.tags_manager.get_all_tags()
        return tags

    def generate_authors(self) -> List[str]:
        """Generate list of authors"""
        author_names = self.authors_manager.get_all_authors()
        return author_names

    def generate_products(self) -> List[str]:
        """Generate list of product names"""
        products = self.products_manager.get_all_products_names()
        return products

    def generate_shops(self) -> List[Dict[str, object]]:
        shop_info = list(self.shop_manager.get_shop_data_generator())
        return shop_info

    def generate_recipe(self) -> List[Dict[str, object]]:
        recipe = [
            {
                'title': self.recipe_manager.get_title(),
                'author': self.authors_manager.get_random_author(),
                'tags': self.tags_manager.get_tags_set(),
                'text': self.recipe_manager.get_text(),
                'portions': self.recipe_manager.get_portions(),
                'products': self.recipe_manager.get_products_weight()
            }
        ]
        return recipe


if __name__ == '__main__':
    from random import sample, randint

    from sweet_grany_app.db_data_generator.tags import Tag
    from sweet_grany_app.db_data_generator.authors import Author
    from sweet_grany_app.db_data_generator.products import Products
    from sweet_grany_app.db_data_generator.shop import Shop
    from sweet_grany_app.db_data_generator.recipe import Recipe
    from sweet_grany_app.db_data_generator.words_base import TAGS, AUTHORS, \
        COOKING_WORDS, SHOPS, PRODUCTS, ADVERBS

    patient = DataGenerator(
        Tag(TAGS),
        Author(AUTHORS),
        Products(PRODUCTS),
        Shop(SHOPS, PRODUCTS),
        Recipe(
            COOKING_WORDS['cooking']['clean'],
            COOKING_WORDS['cooking']['prepare'],
            COOKING_WORDS['cooking']['merge'],
            COOKING_WORDS['cooking']['cook'],
            COOKING_WORDS['cooking']['finalize'],
            ADVERBS,
            sample(PRODUCTS, randint(3, 5))
        )
    )

    print(patient.generate_tags())
    print(patient.generate_authors())
    print(patient.generate_products())
    print(patient.generate_shops())
    print(patient.generate_recipe())
