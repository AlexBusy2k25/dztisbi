from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "sql"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


def setup_database():
    """Создает тестовую БД с данными"""
    conn = sqlite3.connect(DATA_DIR / "tinkoff.db")

    conn.executescript("""
        DROP TABLE IF EXISTS clients;
        CREATE TABLE clients (
            client_id INTEGER PRIMARY KEY,
            client_name TEXT,
            registration_date DATE,
            city TEXT,
            age INTEGER
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
    clients_data = [(i, f'Клиент_{i}', f'2025-0{(i % 12) + 1}-0{(i % 28) + 1}',
                     ['Москва', 'СПб', 'Казань'][i % 3], 25 + (i % 30))
                    for i in range(1, 101)]
    conn.executemany("INSERT INTO clients VALUES (?,?,?,?,?)", clients_data)

    # Транзакции
    start_date = datetime(2025, 1, 1)
    transactions = []
    for i in range(1, 501):
        client_id = random.randint(1, 100)
        days_offset = random.randint(0, 425)
        trans_date = start_date + timedelta(days=days_offset)
        amount = random.uniform(100, 50000)
        category = ['еда', 'одежда', 'техника', 'развлечения', 'транспорт'][random.randint(0, 4)]
        transactions.append((i, client_id, trans_date.date().isoformat(), round(amount, 2), category))

    conn.executemany("INSERT INTO transactions VALUES (?,?,?,?,?)", transactions)

    # Категории
    categories = [(1, 'Электроника'), (2, 'Одежда'), (3, 'Продукты'),
                  (4, 'Книги'), (5, 'Спорт')]
    conn.executemany("INSERT INTO categories VALUES (?,?)", categories)

    # Продукты
    products = []
    for cat_id in range(1, 6):
        for j in range(1, 11):
            prod_id = (cat_id - 1) * 10 + j
            price = random.uniform(100, 50000)
            products.append((prod_id, f'Товар_{prod_id}', cat_id, round(price, 2)))

    conn.executemany("INSERT INTO products VALUES (?,?,?,?)", products)

    # Продажи
    sales = []
    for i in range(1, 301):
        prod_id = random.randint(1, 50)
        days_offset = random.randint(0, 150)
        sale_date = start_date + timedelta(days=days_offset)
        quantity = random.randint(1, 10)
        sales.append((i, prod_id, sale_date.date().isoformat(), quantity))

    conn.executemany("INSERT INTO sales VALUES (?,?,?,?)", sales)

    conn.commit()
    conn.close()
    print("✅ Тестовая БД создана")


def execute_sql_task(task_num):
    """Выполняет SQL из файла и сохраняет результат"""
    sql_file = SQL_DIR / f"task{task_num}.sql"
    if not sql_file.exists():
        print(f"❌ Файл {sql_file} не найден")
        return None

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql = f.read()

    conn = sqlite3.connect(DATA_DIR / "tinkoff.db")
    df = pd.read_sql_query(sql, conn)
    conn.close()

    output_file = OUTPUT_DIR / f"task{task_num}_result.xlsx"
    df.to_excel(output_file, index=False)

    print(f"\n📊 ЗАДАНИЕ {task_num}:")
    print(df.head(10).to_string())
    print(f"✅ Сохранено в {output_file}")

    return df


def create_visualizations():
    """Создает визуализации по результатам"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Аналитика Тинькофф - Дашборд', fontsize=16)

    # График 1: Топ клиентов
    if (OUTPUT_DIR / "task1_result.xlsx").exists():
        df1 = pd.read_excel(OUTPUT_DIR / "task1_result.xlsx")
        top5 = df1.head(5)
        axes[0, 0].barh(top5['client_name'], top5['total_amount'], color='skyblue')
        axes[0, 0].set_title('Топ-5 клиентов по сумме транзакций')
        axes[0, 0].set_xlabel('сумма, руб')

    # График 2: Категории
    if (OUTPUT_DIR / "task2_result.xlsx").exists():
        df2 = pd.read_excel(OUTPUT_DIR / "task2_result.xlsx")
        cat_stats = df2.groupby('category_name')['total_revenue'].sum()
        axes[0, 1].pie(cat_stats.values, labels=cat_stats.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Доля категорий в выручке')

    # График 3: Retention
    if (OUTPUT_DIR / "task3_result.xlsx").exists():
        df3 = pd.read_excel(OUTPUT_DIR / "task3_result.xlsx")

        for cohort in df3['cohort_month'].unique()[:3]:  # берем первые 3 когорты
            cohort_data = df3[df3['cohort_month'] == cohort]
            axes[1, 0].plot(cohort_data['month_number'],
                            cohort_data['retention_rate'],
                            marker='o', label=str(cohort)[:7])

        axes[1, 0].set_title('Retention по когортам (%)')
        axes[1, 0].set_xlabel('месяц')
        axes[1, 0].set_ylabel('retention %')
        axes[1, 0].legend(loc='upper right', fontsize=8)
        axes[1, 0].grid(True, alpha=0.3)

    # График 4: Динамика транзакций
    conn = sqlite3.connect(DATA_DIR / "tinkoff.db")
    df = pd.read_sql_query("""
        SELECT 
            DATE(transaction_date) as date,
            COUNT(*) as trans_count,
            SUM(amount) as total_amount
        FROM transactions
        GROUP BY DATE(transaction_date)
        ORDER BY date
    """, conn)
    conn.close()

    if not df.empty:
        df_last30 = df.tail(30)
        axes[1, 1].plot(range(len(df_last30)), df_last30['total_amount'].values,
                        marker='o', linestyle='-', color='green', markersize=4)
        axes[1, 1].set_title('Динамика суммы транзакций (последние 30 дней)')
        axes[1, 1].set_xlabel('день')
        axes[1, 1].set_ylabel('сумма, руб')
        axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    dashboard_path = OUTPUT_DIR / 'dashboard.png'
    plt.savefig(dashboard_path, dpi=100, bbox_inches='tight')
    print(f"\n📊 Дашборд сохранен в {dashboard_path}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 TINKOFF ANALYTICS (SQL ЗАДАНИЯ)")
    print("=" * 60)

    setup_database()

    for i in range(1, 4):
        execute_sql_task(i)

    create_visualizations()

    print("\n" + "=" * 60)
    print("✅ ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ")
    print(f"📁 Результаты в папке: {OUTPUT_DIR}")