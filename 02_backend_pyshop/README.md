## 02_backend_pyshop — сервис чеков (PyShop)

**Направление**: backend (Python, FastAPI, PostgreSQL)  
**Компания по заданию**: PyShop / «ФорФар»

### Описание

Упрощённая реализация тестового задания PyShop: сервис, который позволяет создавать заказы и связанные с ними чеки для кухни и клиента.  
Вместо Django здесь используется **FastAPI** + **PostgreSQL** + **SQLAlchemy**, но структура и сущности (принтер, чек) соответствуют постановке задачи.

### Локальный запуск

1. **Создать виртуальное окружение**:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. **Установить зависимости**:

```bash
pip install -r requirements.txt
```

3. **Создать `.env`**:

```bash
copy .env.example .env
```

По умолчанию:

- `POSTGRES_HOST=localhost`
- `POSTGRES_PORT=5432`
- `POSTGRES_DB=pyshop`
- `POSTGRES_USER=pyshop`
- `POSTGRES_PASSWORD=pyshop`

4. Запустить PostgreSQL (можно через Docker, см. ниже) и применить создание таблиц (они создаются автоматически при старте приложения).

5. **Запуск приложения**:

```bash
uvicorn app.main:app --reload
```

### Запуск в Docker

```bash
docker-compose up --build
```

После старта API будет доступно по адресу `http://127.0.0.1:8000`.

### Основные эндпоинты

- `POST /orders/` — создать заказ и сгенерировать чеки для точки (упрощённо).
- `GET /checks/` — получить список чеков.

### Линтеры и стиль

Проверка из корня репозитория:

```bash
flake8 02_backend_pyshop
isort --check-only 02_backend_pyshop
```

