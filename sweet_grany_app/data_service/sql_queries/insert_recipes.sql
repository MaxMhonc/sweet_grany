INSERT INTO recipes (title, text, portions, author_id)
VALUES ('<plaseholder>', '<plaseholder>', '<plaseholder>',
        (SELECT author_id FROM authors WHERE name = '<plaseholder>'));