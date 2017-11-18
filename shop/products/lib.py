
from django.db import connection


def refresh_products_logos(product_ids):

    cursor = connection.cursor()

    sql = """
            UPDATE `products_product`
            SET `products_product`.`logo` = (
                SELECT `products_productimage`.`file`
                FROM `products_productimage`
                WHERE `products_product`.`id`=`products_productimage`.`product_id`
                ORDER BY `products_productimage`.`order`
                LIMIT 1
            )
            WHERE `products_product`.`id` IN %(product_ids)s
        """

    try:
        cursor.execute(sql, {
            'product_ids': product_ids
        })
    finally:
        cursor.close()
