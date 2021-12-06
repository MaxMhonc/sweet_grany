INSERT INTO products_recipe (recipe_id, product_id, amount_whole_part, amount_decimal_part)
VALUES ((SELECT recipe_id FROM recipes WHERE title = '<plaseholder>'),
        (SELECT product_id FROM products WHERE name = '<plaseholder>'),
        '<plaseholder>', '<plaseholder>');