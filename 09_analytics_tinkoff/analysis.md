## Теоретические вопросы по SQL

**1. Может ли измениться результат запроса, если в `LEFT JOIN` поменять таблицы местами?**  
Да. `LEFT JOIN` некоммутативен: `A LEFT JOIN B` и `B LEFT JOIN A` дают разный набор строк и `NULL`‑ов, потому что в одном случае сохраняются все строки `A`, а в другом — все строки `B`.

**2. Сколько будет `5 + NULL`?**  
Результат — `NULL`. Любая арифметика с `NULL` в стандартном SQL даёт `NULL` (неизвестно).

**3. Можно ли делать `JOIN` таблицы саму на себя?**  
Да, это **self join**. Часто используется для иерархий, сравнения строк между собой и т.п.; при этом обязательно использовать алиасы таблицы.

**4. Может ли `ORDER BY` приводить к уменьшению числа строк в результате выполнения?**  
Нет. `ORDER BY` только меняет порядок строк, их количество не уменьшает (уменьшают количество строк конструкции `WHERE`, `DISTINCT`, `GROUP BY`, `LIMIT` и т.п.).

**5. При каких типах соединения условие из `WHERE` можно перенести в `ON` с гарантированным сохранением результата запроса?**  
Для **внутреннего соединения** (`INNER JOIN`) и эквивалентного `CROSS JOIN` + `WHERE`.  
Для `LEFT/RIGHT/FULL JOIN` перенос предиката из `WHERE` в `ON` меняет семантику (фильтрацию `NULL`‑строк) и результат.

**6. Какой из операторов: `SELECT`, `FROM`, `WHERE`, `GROUP BY` — выполняется последним при обработке запроса?**  
Логический порядок такой: `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`.  
Из перечисленных — **`SELECT`** выполняется последним.

**7. Какие функции умеют возвращать значения из предыдущих/последующих строк для заданной строки таблицы?**  
Оконные функции **`LAG()`** и **`LEAD()`** (также родственники: `FIRST_VALUE`, `LAST_VALUE`, но именно LAG/LEAD возвращают значения из прошлых/следующих строк).

**8. Какое минимальное и максимальное количество записей может выдать `FULL JOIN` таблицы на 10 строк с таблицей на 100 строк?**  
- Минимум — `max(10, 100) = 100` (каждая строка обеих таблиц нашла себе соответствие).  
- Максимум — `10 + 100 = 110` (ни одна строка первой таблицы не сопоставилась со второй и наоборот).

## Пример SQL для топ‑5 товаров в первых заказах пользователей СПб (15–30 августа)

Предполагаем схему:

- `orders(id, user_id, created_at, city)`  
- `order_lines(order_id, product_id, quantity)`  
- `products(id, name)`

```sql
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
```

