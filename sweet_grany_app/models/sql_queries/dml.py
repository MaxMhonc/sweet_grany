INSERT_AUTHORS = """INSERT INTO authors (name) VALUES (:name);"""

INSERT_PRODUCTS = """INSERT INTO products (name) VALUES (:name);"""

INSERT_SHOPS = """INSERT INTO shops (name) VALUES (:name);"""

INSERT_SHOP_PRODUCTS = """
    INSERT INTO products_shop
    (product_id, shop_id, price)
    VALUES ((SELECT id FROM products WHERE name = :prod_name),
    (SELECT id FROM shops WHERE name = :shop_name),
    :price);
"""

INSERT_RECIPE = """
    INSERT INTO recipes (title, text, portions, author_id)
    VALUES (:title, :text, :portions,
    (SELECT id FROM authors WHERE name = :author_name));
"""

INSERT_RECIPE_TAGS = """
    INSERT INTO tags (name, recipe_id)
    VALUES (:tag_name,
    (SELECT id FROM recipes WHERE title = :title));
"""

INSERT_RECIPE_PRODUCTS = """
    INSERT INTO products_recipe
    (recipe_id, product_id, weight)
    VALUES (
    (SELECT id FROM recipes WHERE title = :title),
    (SELECT id FROM products WHERE name = :name),
    :weight);
"""
