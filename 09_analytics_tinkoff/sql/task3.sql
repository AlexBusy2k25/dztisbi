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
        COUNT(DISTINCT t.client_id) as clients
    FROM first_orders f
    JOIN transactions t ON f.client_id = t.client_id
    GROUP BY f.cohort_month, activity_month
),
cohort_size AS (
    SELECT
        cohort_month,
        clients as size
    FROM cohort_data
    WHERE cohort_month = activity_month
)
SELECT
    cd.cohort_month,
    cd.activity_month,
    cd.clients,
    cs.size as cohort_size,
    ROUND(100.0 * cd.clients / cs.size, 2) as retention_rate,
    (JULIANDAY(cd.activity_month) - JULIANDAY(cd.cohort_month)) / 30 as month_number
FROM cohort_data cd
JOIN cohort_size cs ON cd.cohort_month = cs.cohort_month
ORDER BY cd.cohort_month, cd.activity_month;