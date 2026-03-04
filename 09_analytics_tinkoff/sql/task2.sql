WITH product_sales AS (
    SELECT
        p.category_id,
        c.category_name,
        p.product_id,
        p.product_name,
        SUM(s.quantity) as total_sold,
        SUM(s.quantity * p.price) as total_revenue
    FROM products p
    JOIN sales s ON p.product_id = s.product_id
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY p.category_id, p.product_id
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY total_sold DESC) as rank
    FROM product_sales
)
SELECT
    category_name,
    product_name,
    total_sold,
    ROUND(total_revenue, 2) as total_revenue
FROM ranked
WHERE rank <= 3
ORDER BY category_name, rank;