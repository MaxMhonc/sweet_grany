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

GET_RECIPE_PRICES = """
    SELECT sum(max_product_cost) as max_recipe_cost,
           sum(min_product_cost) as min_recipe_cost
    FROM (
             SELECT pr.weight * max(ps.price) as max_product_cost,
                    pr.weight * min(ps.price) as min_product_cost
             FROM products_shop ps
                      INNER JOIN products p ON p.id = ps.product_id
                      INNER JOIN products_recipe pr ON p.id = pr.product_id
             WHERE pr.recipe_id = (SELECT id FROM recipes WHERE title = :title)
             GROUP BY p.id, pr.weight
         ) as recipe_prods_prices;
"""

GET_CHEAPER_RECIPE_COMPONENTS_PRICE = """
WITH products_min_price AS (
    SELECT product_id,
           min(price) as min_price
    FROM products_shop
    GROUP BY product_id
),
     products_shops_min_price AS (
         SELECT ps.product_id,
                pmp.min_price,
                ps.shop_id
         FROM products_shop ps
                  INNER JOIN products_min_price AS pmp
                             ON ps.product_id = pmp.product_id
                             AND ps.price = pmp.min_price
     )
SELECT p.name                       as product,
       s.name                       as shop,
       psmp.min_price               as price,
       pr.weight                    as weight,
       (pr.weight * psmp.min_price) as cost
FROM recipes
         INNER JOIN products_recipe pr ON recipes.id = pr.recipe_id
         INNER JOIN products p ON p.id = pr.product_id
         INNER JOIN products_shops_min_price psmp ON p.id = psmp.product_id
         INNER JOIN shops s ON s.id = psmp.shop_id
WHERE pr.recipe_id = (SELECT id FROM recipes WHERE title = :title);
"""
