SELECT
    c.client_id,
    c.client_name,
    COUNT(t.transaction_id) as trans_count,
    SUM(t.amount) as total_amount
FROM clients c
JOIN transactions t ON c.client_id = t.client_id
GROUP BY c.client_id
ORDER BY total_amount DESC
LIMIT 10;