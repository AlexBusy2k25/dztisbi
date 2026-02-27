from pathlib import Path

import pandas as pd
import sqlalchemy as sa


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


def load_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    engine = sa.create_engine(f"sqlite:///{DB_PATH}")
    with engine.begin() as connection:
        pl = pd.read_sql("SELECT * FROM pl", connection)
        campaign = pd.read_sql("SELECT * FROM campaign", connection)
    return pl, campaign


def main() -> None:
    if not DB_PATH.exists():
        print(f"Файл {DB_PATH} не найден. Положите database.db в папку {BASE_DIR}.")
        return

    pl, campaign = load_tables()

    agg1 = (
        pl.groupby(["segment", "period", "product"])
        .agg(avg_pl=("pl", "mean"), clients=("client_id", "nunique"))
        .reset_index()
    )
    print("Средний ЧОД и количество клиентов по продуктам/сегментам/периодам:")
    print(agg1.head())


if __name__ == "__main__":
    main()

