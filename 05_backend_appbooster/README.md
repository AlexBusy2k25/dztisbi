## 05_backend_appbooster — сервис A/B‑экспериментов (AppBooster)

**Направление**: backend (Python, FastAPI, PostgreSQL)  
**Компания по заданию**: AppBooster

### Описание

Упрощённая версия тестового задания AppBooster: REST‑сервис, который по заголовку `Device-Token` возвращает набор экспериментов и выбранные варианты, фиксируя распределение пользователей по группам.

### Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

### Запуск в Docker

```bash
docker-compose up --build
```

### Основной эндпоинт

- `GET /experiments/` — читает заголовок `Device-Token` и возвращает JSON с экспериментами:
  - `button_color` — один из `#FF0000`, `#00FF00`, `#0000FF`;
  - `price` — одно из значений `10`, `20`, `50`, `5`.

