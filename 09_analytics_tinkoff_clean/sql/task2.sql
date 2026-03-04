SELECT
    cat.category_name,
    p.product_name,
    SUM(s.quantity) as total_sold,
    SUM(s.quantity * p.price) as revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name, p.product_name
ORDER BY cat.category_name, revenue DESC;