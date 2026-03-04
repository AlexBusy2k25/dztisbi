-- ЗАДАНИЕ 3: Анализ Retention (удержание клиентов)
-- Рассчитать когортный анализ по месяцам первого заказа

WITH first_orders AS (
    SELECT
        client_id,
        MIN(DATE(transaction_date, 'start of month')) as cohort_month
    FROM transactions
    GROUP BY client_id
),
cohort_data AS (
    SELECT
        f.cohort_month,
        DATE(t.transaction_date, 'start of month') as activity_month,
        COUNT(DISTINCT t.client_id) as clients_count
    FROM first_orders f
    JOIN transactions t ON f.client_id = t.client_id
    GROUP BY f.cohort_month, DATE(t.transaction_date, 'start of month')
),
cohort_size AS (
    SELECT
        cohort_month,
        clients_count as cohort_size
    FROM cohort_data
    WHERE cohort_month = activity_month
),
retention AS (
    SELECT
        cd.cohort_month,
        cd.activity_month,
        cd.clients_count,
        cs.cohort_size,
        ROUND(100.0 * cd.clients_count / cs.cohort_size, 2) as retention_rate,
        JULIANDAY(cd.activity_month) - JULIANDAY(cd.cohort_month) as months_diff
    FROM cohort_data cd
    JOIN cohort_size cs ON cd.cohort_month = cs.cohort_month
)
SELECT
    cohort_month,
    activity_month,
    clients_count,
    cohort_size,
    retention_rate || '%' as retention_rate,
    months_diff || ' мес.' as period
FROM retention
WHERE months_diff >= 0
ORDER BY cohort_month, activity_month;