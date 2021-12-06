INSERT INTO tags_recipes (recipe_id, tag_id)
VALUES ((SELECT recipe_id FROM recipes WHERE title = '<plaseholder>'),
        (SELECT tag_id FROM tags WHERE name = '<plaseholder>'));