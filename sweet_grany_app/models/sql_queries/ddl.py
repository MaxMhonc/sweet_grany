CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS authors
    (
        id   SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS recipes
    (
        id        SERIAL PRIMARY KEY,
        title     VARCHAR(200) NOT NULL UNIQUE,
        text      TEXT         NOT NULL,
        portions  SMALLINT CHECK ( portions > 0 ),
        author_id INT,
        CONSTRAINT fk_author
            FOREIGN KEY (author_id)
                REFERENCES authors (id)
                ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS tags
    (
        id        SERIAL PRIMARY KEY,
        name      VARCHAR(100) NOT NULL,
        recipe_id INT,
        CONSTRAINT fk_recipe
            FOREIGN KEY (recipe_id)
                REFERENCES recipes (id)
                ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS shops
    (
        id   SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS products
    (
        id   SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS products_recipe
    (
        recipe_id  INT,
        product_id INT,
        weight     NUMERIC NOT NULL CHECK ( weight > 0 ),
        CONSTRAINT fk_recipe
            FOREIGN KEY (recipe_id)
                REFERENCES recipes (id)
                ON DELETE CASCADE,
        CONSTRAINT fk_product
            FOREIGN KEY (product_id)
                REFERENCES products (id)
                ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS products_shop
    (
        product_id INT,
        shop_id    INT,
        price      NUMERIC NOT NULL CHECK ( price > 0 ),
        CONSTRAINT fk_products
            FOREIGN KEY (product_id)
                REFERENCES products (id)
                ON DELETE CASCADE,
        CONSTRAINT fk_shop
            FOREIGN KEY (shop_id)
                REFERENCES shops (id)
                ON DELETE CASCADE
    );

"""

DROP_TABLES = """
    DROP TABLE IF EXISTS
        recipes,
        products,
        products_recipe,
        authors,
        shops,
        products_shop,
        tags;
"""
