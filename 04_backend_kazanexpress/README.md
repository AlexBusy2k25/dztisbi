## 04_backend_kazanexpress — админка магазина (KazanExpress)

**Направление**: backend (Python, FastAPI, PostgreSQL)  
**Компания по заданию**: KazanExpress

### Описание

Упрощённая версия тестового задания KazanExpress: API для управления магазинами, товарами и категориями.  
Вместо Django admin используется FastAPI + SQLAlchemy, но модели `Shop`, `Product`, `Category` и основные операции (список, поиск, фильтры) отражают требования оригинала.

### Локальный запуск

1. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Создайте `.env`:

```bash
copy .env.example .env
```

3. Запустите PostgreSQL (можно через `docker-compose`, см. ниже) и приложение:

```bash
uvicorn app.main:app --reload
```

Swagger UI будет доступен по адресу `http://127.0.0.1:8003/docs`.

### Запуск в Docker

```bash
docker-compose up --build
```

Будут подняты:

- PostgreSQL с БД `kazanexpress`
- API FastAPI на порту `8003`

### Основные эндпоинты (упрощённо)

- `POST /shops/`, `GET /shops/` — создание и список магазинов (фильтрация по названию).
- `POST /products/`, `GET /products/` — создание и список товаров (фильтр по активным, поиск по названию, сортировка по цене).
- `POST /categories/`, `GET /categories/` — создание и список категорий.

