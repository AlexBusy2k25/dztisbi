-- Пример SQL для задания Самокат Аналитик Данных
-- Предполагаем таблицы:
-- warehouses(id, name, city, ...)
-- products(id, name, category, ...)
-- orders(id, user_id, warehouse_id, created_at, city, ...)
-- order_lines(id, order_id, product_id, quantity, price, ...)

-- Задача 2. user_id, у которых 1–15 августа есть два любых корма для животных,
-- кроме конкретного товара "Корм Kitekat для кошек, с кроликом в соусе, 85 г"

WITH august_orders AS (
    SELECT
        o.id,
        o.user_id
    FROM orders AS o
    WHERE o.created_at >= DATE '2023-08-01'
      AND o.created_at <  DATE '2023-08-16'
),
pet_food AS (
    SELECT
        p.id AS product_id
    FROM products AS p
    WHERE p.category = 'Корма для животных'
      AND p.name <> 'Корм Kitekat для кошек, с кроликом в соусе, 85 г'
),
user_pet_food AS (
    SELECT
        ao.user_id,
        COUNT(DISTINCT ol.product_id) AS distinct_pet_foods
    FROM august_orders AS ao
    JOIN order_lines AS ol
      ON ol.order_id = ao.id
    JOIN pet_food AS pf
      ON pf.product_id = ol.product_id
    GROUP BY ao.user_id
)
SELECT
    user_id
FROM user_pet_food
WHERE distinct_pet_foods >= 2;


-- Задача 3. Топ‑5 самых частых товаров в первых заказах пользователей в СПб (15–30 августа)

WITH first_orders AS (
    SELECT
        o.user_id,
        MIN(o.created_at) AS first_order_at
    FROM orders AS o
    WHERE
        o.city = 'Санкт-Петербург'
        AND o.created_at >= DATE '2023-08-15'
        AND o.created_at <  DATE '2023-08-31'
    GROUP BY o.user_id
),
first_orders_ids AS (
    SELECT
        o.id,
        o.user_id
    FROM orders AS o
    JOIN first_orders AS f
      ON  o.user_id = f.user_id
      AND o.created_at = f.first_order_at
)
SELECT
    p.id          AS product_id,
    p.name        AS product_name,
    COUNT(*)      AS first_order_count
FROM order_lines AS ol
JOIN first_orders_ids AS fo
  ON ol.order_id = fo.id
JOIN products AS p
  ON ol.product_id = p.id
GROUP BY p.id, p.name
ORDER BY first_order_count DESC
LIMIT 5;

