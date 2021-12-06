INSERT INTO products_shop (product_id, shop_id, price_whole_part, price_decimal_part)
VALUES ((SELECT product_id FROM products WHERE name = '<plaseholder>'),
        (SELECT shop_id FROM shops WHERE name = '<plaseholder>'),
        '<plaseholder>', '<plaseholder>');