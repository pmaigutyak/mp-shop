
INSERT INTO products_image ("order", file, product_id)
SELECT "order", file, product_id
FROM products_productimage
