INSERT INTO products_product (
    id,
    price_retail,
    price_wholesale,
    price_usd,
    price_eur,
    price_uah,
    initial_currency,
    is_visible,
    name,
    name_uk,
    name_ru,
    code,
    description,
    description_uk,
    description_ru,
    logo,
    created,
    availability_id,
    category_id,
    manufacturer_id
) SELECT
    id,
    price,
    0,
    0,
    0,
    0,
    980,
    is_visible,
    name,
    name_uk,
    name_ru,
    code,
    description,
    description_uk,
    description_ru,
    '',
    NULL ,
    1,
    category_id,
    NULL
FROM _products_product