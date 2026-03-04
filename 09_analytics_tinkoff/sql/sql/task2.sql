-- ЗАДАНИЕ 2: Анализ продуктов и категорий
-- Найти продукты, которые продаются лучше всего в каждой категории

WITH category_stats AS (
    SELECT
        p.category_id,
        c.category_name,
        p.product_id,
        p.product_name,
        SUM(s.quantity) as total_sold,
        SUM(s.quantity * p.price) as total_revenue,
        COUNT(DISTINCT s.sale_id) as sales_count,
        AVG(s.quantity) as avg_quantity_per_sale
    FROM products p
    JOIN sales s ON p.product_id = s.product_id
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY p.category_id, c.category_name, p.product_id, p.product_name
),
ranked_products AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY total_sold DESC) as rank_in_category,
        ROUND(100.0 * total_sold / SUM(total_sold) OVER (PARTITION BY category_id), 2) as share_in_category
    FROM category_stats
)
SELECT
    category_id,
    category_name,
    product_id,
    product_name,
    total_sold,
    total_revenue,
    sales_count,
    avg_quantity_per_sale,
    share_in_category || '%' as share_in_category
FROM ranked_products
WHERE rank_in_category <= 3
ORDER BY category_id, rank_in_category;