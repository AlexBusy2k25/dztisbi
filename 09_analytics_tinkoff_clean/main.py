import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import random
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
SQL_DIR = BASE_DIR / "sql"

OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


def setup_database():
    """Создаёт тестовую БД"""
    conn = sqlite3.connect(DATA_DIR / "tinkoff.db")

    conn.executescript("""
        DROP TABLE IF EXISTS clients;
        CREATE TABLE clients (
            client_id INTEGER PRIMARY KEY,
            client_name TEXT,
            registration_date DATE,
            city TEXT
        );

        DROP TABLE IF EXISTS transactions;
        CREATE TABLE transactions (
            transaction_id INTEGER PRIMARY KEY,
            client_id INTEGER,
            transaction_date DATE,
            amount REAL,
            category TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(client_id)
        );

        DROP TABLE IF EXISTS products;
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category_id INTEGER,
            price REAL
        );

        DROP TABLE IF EXISTS categories;
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT
        );

        DROP TABLE IF EXISTS sales;
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            sale_date DATE,
            quantity INTEGER,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)

    # Клиенты
    clients = [(i, f'Клиент_{i}', f'2025-01-{(i % 28) + 1:02d}',
                ['Москва', 'СПб', 'Казань', 'Екб'][i % 4]) for i in range(1, 51)]
    conn.executemany("INSERT INTO clients VALUES (?,?,?,?)", clients)

    # Транзакции
    start = datetime(2025, 1, 1)
    transactions = []
    for i in range(1, 201):
        client = random.randint(1, 50)
        days = random.randint(0, 425)
        date = start + timedelta(days=days)
        amount = round(random.uniform(100, 50000), 2)
        cat = ['еда', 'одежда', 'техника', 'развлечения'][random.randint(0, 3)]
        transactions.append((i, client, date.date(), amount, cat))
    conn.executemany("INSERT INTO transactions VALUES (?,?,?,?,?)", transactions)

    # Категории
    categories = [(1, 'Электроника'), (2, 'Одежда'), (3, 'Продукты'), (4, 'Книги')]
    conn.executemany("INSERT INTO categories VALUES (?,?)", categories)

    # Продукты
    products = []
    for cat in range(1, 5):
        for j in range(1, 6):
            pid = (cat - 1) * 5 + j
            price = round(random.uniform(500, 30000), 2)
            products.append((pid, f'Товар_{pid}', cat, price))
    conn.executemany("INSERT INTO products VALUES (?,?,?,?)", products)

    # Продажи
    sales = []
    for i in range(1, 151):
        pid = random.randint(1, 20)
        days = random.randint(0, 150)
        date = start + timedelta(days=days)
        qty = random.randint(1, 10)
        sales.append((i, pid, date.date(), qty))
    conn.executemany("INSERT INTO sales VALUES (?,?,?,?)", sales)

    conn.commit()
    conn.close()
    print("✅ Тестовая БД создана")


def execute_task1():
    """Топ-10 клиентов по сумме транзакций"""
    conn = sqlite3.connect(DATA_DIR / "tinkoff.db")
    query = """
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
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df.to_excel(OUTPUT_DIR / 'task1_top_clients.xlsx', index=False)
    print("\n📊 Топ-10 клиентов:")
    print(df.to_string(index=False))
    return df


def execute_task2():
    """Анализ продаж по категориям"""
    conn = sqlite3.connect(DATA_DIR / "tinkoff.db")
    query = """
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
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df.to_excel(OUTPUT_DIR / 'task2_category_sales.xlsx', index=False)
    print("\n📊 Продажи по категориям:")
    print(df.head(10).to_string(index=False))
    return df


def create_dashboard(df1, df2):
    """Создаёт дашборд"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Аналитика Тинькофф - Дашборд', fontsize=16)

    # Топ клиентов
    top5 = df1.head(5)
    axes[0, 0].barh(top5['client_name'], top5['total_amount'], color='skyblue')
    axes[0, 0].set_title('Топ-5 клиентов')
    axes[0, 0].set_xlabel('Сумма, руб')

    # Доля категорий
    cat_rev = df2.groupby('category_name')['revenue'].sum()
    axes[0, 1].pie(cat_rev.values, labels=cat_rev.index, autopct='%1.1f%%')
    axes[0, 1].set_title('Доля категорий в выручке')

    # Количество транзакций по месяцам
    conn = sqlite3.connect(DATA_DIR / "tinkoff.db")
    query = """
    SELECT 
        strftime('%Y-%m', transaction_date) as month,
        COUNT(*) as trans_count,
        SUM(amount) as total
    FROM transactions
    GROUP BY month
    ORDER BY month;
    """
    df_month = pd.read_sql_query(query, conn)
    conn.close()

    axes[1, 0].plot(df_month['month'], df_month['total'], marker='o')
    axes[1, 0].set_title('Динамика выручки')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Статистика
    stats = f"""
    Всего клиентов: 50
    Всего транзакций: 200
    Средний чек: {df1['total_amount'].mean():.0f} руб
    """
    axes[1, 1].text(0.1, 0.5, stats, fontsize=14, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'dashboard.png', dpi=150, bbox_inches='tight')
    print(f"\n📊 Дашборд сохранён")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 TINKOFF ANALYTICS")
    print("=" * 60)

    setup_database()
    df1 = execute_task1()
    df2 = execute_task2()
    create_dashboard(df1, df2)

    print("\n" + "=" * 60)
    print("✅ Все задачи выполнены")
    print(f"📁 Результаты в папке: {OUTPUT_DIR}")