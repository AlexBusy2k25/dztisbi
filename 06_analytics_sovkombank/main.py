from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def transform_registry() -> None:
    """Пример функции для преобразования реестра (задача 1)."""
    source_path = DATA_DIR / "registry_source.xlsx"
    if not source_path.exists():
        print(f"Файл {source_path} не найден, пропускаю задачу 1.")
        return

    df = pd.read_excel(source_path)
    # Здесь можно добавить реальную логику преобразования под нужный формат.
    print("Первые строки реестра:")
    print(df.head())


def mark_cities_in_addresses() -> None:
    """Пример функции для задачи 2 — определение городов в адресах."""
    addresses_path = DATA_DIR / "addresses.xlsx"
    cities_path = DATA_DIR / "cities.xlsx"

    if not addresses_path.exists() or not cities_path.exists():
        print("Файлы с адресами/городами не найдены, пропускаю задачу 2.")
        return

    addresses = pd.read_excel(addresses_path)
    cities = pd.read_excel(cities_path)

    city_list = cities["city"].dropna().astype(str).tolist()

    def find_city(address: str) -> str | None:
        if not isinstance(address, str):
            return None
        for city in city_list:
            if city in address:
                return city
        return None

    addresses["found_city"] = addresses["address"].apply(find_city)
    print("Примеры адресов с найденными городами:")
    print(addresses.head())


if __name__ == "__main__":
    transform_registry()
    mark_cities_in_addresses()

