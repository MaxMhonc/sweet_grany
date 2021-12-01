CREATE_ALL_TABLES = \
    """
CREATE TABLE IF NOT EXISTS tags
(
    tag_id SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS shops
(
    shop_id SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS authors
(
    author_id SERIAL PRIMARY KEY,
    name      VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS recipes
(
    recipe_id SERIAL PRIMARY KEY,
    title     VARCHAR(200) NOT NULL,
    text      TEXT         NOT NULL,
    portions  SMALLINT CHECK ( portions > 0 ),
    author_id INT,
    CONSTRAINT fk_author
        FOREIGN KEY (author_id)
            REFERENCES authors (author_id)
            ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS products
(
    product_id SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS products_recipe
(
    recipe_id           INT,
    product_id          INT,
    amount_whole_part   INT NOT NULL CHECK ( amount_whole_part >= 0 ),
    amount_decimal_part INT CHECK ( amount_whole_part >= 0 ),
    CONSTRAINT fk_recipe
        FOREIGN KEY (recipe_id)
            REFERENCES recipes (recipe_id)
            ON DELETE CASCADE,
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
            REFERENCES products (product_id)
            ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS products_shop
(
    product_id         INT,
    shop_id            INT,
    price_whole_part   INT NOT NULL CHECK ( price_whole_part >= 0 ),
    price_decimal_part INT CHECK ( price_decimal_part >= 0 ),
    CONSTRAINT fk_products
        FOREIGN KEY (product_id)
            REFERENCES products (product_id)
            ON DELETE CASCADE,
    CONSTRAINT fk_shop
        FOREIGN KEY (shop_id)
            REFERENCES shops (shop_id)
            ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS tags_recipes
(
    recipe_id         INT,
    tag_id            INT,
    CONSTRAINT fk_recipe
        FOREIGN KEY (recipe_id)
            REFERENCES recipes (recipe_id)
            ON DELETE CASCADE,
    CONSTRAINT fk_tag
        FOREIGN KEY (tag_id)
            REFERENCES tags (tag_id)
            ON DELETE CASCADE
);
    """

DROP_ALL_TABLES = \
    """
    DROP TABLE IF EXISTS
    recipes,
    products,
    products_recipe,
    authors,
    shops,
    products_shop,
    tags,
    tags_recipes;
    """
