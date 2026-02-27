## 03_backend_uptrader — сервис древовидного меню (UpTrader)

**Направление**: backend (Python, FastAPI, PostgreSQL)  
**Компания по заданию**: UpTrader

### Описание

Упрощённая реализация тестового задания UpTrader: хранение древовидных меню в БД и отдача структуры меню по имени.  
Вместо Django template tag используется REST‑API на FastAPI, но сущности (меню, пункты меню, связи родитель/ребёнок) повторяют постановку.

### Локальный запуск

1. Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Создайте файл `.env`:

```bash
copy .env.example .env
```

3. Поднимите PostgreSQL (можно через Docker, см. ниже) и запустите приложение:

```bash
uvicorn app.main:app --reload
```

### Запуск в Docker

```bash
docker-compose up --build
```

После запуска API будет доступно по адресу `http://127.0.0.1:8002`.

### Основные эндпоинты

- `POST /menu-items/` — создать пункт меню.
- `GET /menus/{menu_name}` — получить дерево меню по имени.

