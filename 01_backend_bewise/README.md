## 01_backend_bewise — сервис вопросов викторины (Bewise)

**Направление**: backend (Python, FastAPI, PostgreSQL)  
**Компания по заданию**: Bewise

### Описание

Проект реализует тестовое задание Bewise: REST‑сервис, который принимает POST‑запрос с количеством вопросов, забирает вопросы с публичного API `https://jservice.io/api/random`, сохраняет их в PostgreSQL, избегая дублей, и возвращает последний сохранённый вопрос.

### Локальный запуск

1. **Создать виртуальное окружение** (Python 3.11+):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. **Установить зависимости**:

```bash
pip install -r requirements.txt
```

3. **Настроить переменные окружения**:

Скопируйте файл `.env.example` в `.env` и при необходимости измените значения:

```bash
copy .env.example .env
```

По умолчанию проект ожидает, что Postgres доступен по адресу:

- `POSTGRES_HOST=localhost`
- `POSTGRES_PORT=5432`
- `POSTGRES_DB=bewise`
- `POSTGRES_USER=bewise`
- `POSTGRES_PASSWORD=bewise`

4. **Запустить PostgreSQL** (можно через Docker, см. ниже) и применить миграции:

```bash
alembic upgrade head
```

5. **Запустить приложение**:

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`.

Интерактивная документация:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Запуск в Docker

1. Убедитесь, что установлен Docker и docker-compose.

2. В корне проекта `01_backend_bewise` выполните:

```bash
docker-compose up --build
```

Это поднимет:

- контейнер с PostgreSQL
- контейнер с приложением FastAPI

После успешного запуска API будет доступно по адресу `http://127.0.0.1:8000`.

### Основные эндпоинты

- `POST /questions/` — принимает JSON вида `{"questions_num": 3}`, запрашивает указанное количество уникальных вопросов у `jservice.io`, сохраняет их в БД и возвращает **предыдущий** сохранённый вопрос (или пустой объект, если его нет).
- `GET /questions/last` — возвращает последний сохранённый вопрос в БД (или пустой объект).

### Линтеры и стиль кода

- Стиль кода: **PEP8**, **wemake-python-styleguide**
- Анализатор кода: **flake8**
- Упорядочивание импортов: **isort**

Проверка стиля (из корня репозитория):

```bash
flake8 01_backend_bewise
isort --check-only 01_backend_bewise
```

