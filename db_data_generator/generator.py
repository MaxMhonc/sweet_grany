from random import choice

from db_data_generator.words_base import COOKING_WORDS, ADVERBS
from db_data_generator.products import Products
from db_data_generator.recipe import Recipe


prods = Products(COOKING_WORDS['products'])
products = prods.generate_products()
product_names = [prod[0] for prod in products]
recipe = Recipe(
        COOKING_WORDS['cooking']['clean'],
        COOKING_WORDS['cooking']['prepare'],
        COOKING_WORDS['cooking']['merge'],
        COOKING_WORDS['cooking']['cook'],
        COOKING_WORDS['cooking']['finalize'],
        product_names
    )
title = (f' {choice(ADVERBS)} '.join(product_names)).capitalize()
product_list = '\n'.join([f'{prod[0]} - {prod[1]} kg' for prod in products])
delimeter = '\n' + '-' * 100 + '\n'
print(delimeter.join([title, recipe.get_text(), product_list]))
