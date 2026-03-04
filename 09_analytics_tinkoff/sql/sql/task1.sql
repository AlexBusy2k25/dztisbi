-- ЗАДАНИЕ 1: Анализ клиентов и транзакций
-- Найти топ-10 клиентов по сумме транзакций за последний месяц

WITH last_month AS (
    SELECT
        DATE('now', '-1 month') as start_date,
        DATE('now') as end_date
),
client_transactions AS (
    SELECT
        c.client_id,
        c.client_name,
        COUNT(t.transaction_id) as transactions_count,
        SUM(t.amount) as total_amount,
        AVG(t.amount) as avg_amount,
        MIN(t.amount) as min_amount,
        MAX(t.amount) as max_amount
    FROM clients c
    JOIN transactions t ON c.client_id = t.client_id
    CROSS JOIN last_month lm
    WHERE t.transaction_date BETWEEN lm.start_date AND lm.end_date
    GROUP BY c.client_id, c.client_name
)
SELECT
    client_id,
    client_name,
    transactions_count,
    ROUND(total_amount, 2) as total_amount,
    ROUND(avg_amount, 2) as avg_amount,
    min_amount,
    max_amount,
    ROUND(100.0 * total_amount / SUM(total_amount) OVER(), 2) as share_percent
FROM client_transactions
ORDER BY total_amount DESC
LIMIT 10;