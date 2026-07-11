# Шаблон для однослойных проектов

## 🏗 Архитектура

### Компоненты:

* **API сервис (FastAPI)**
  Обрабатывает HTTP-запросы и работает с БД

* **PostgreSQL**
  Хранение событий

* **Adminer**
  GUI для работы с БД

---


## 🧪 Тестирование API

👉 **Swagger UI FastAPI**

После запуска:

```
http://localhost:8000/docs
```

Там:

* можно выполнять все запросы
* задавать headers (`X-API-Key`, `Idempotency-Key`)
* удобно смотреть ответы

---

## 🚀 Запуск проекта

### 1. Подготовка

Создать `.env`:

```
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=db

API_KEY=test_api_key

BROKER_HOST=rabbitmq
BROKER_PORT=5672
BROKER_USER=guest
BROKER_PASS=guest
```

---

### 2. Запуск

```bash
docker-compose up --build
```

---

### 3. Доступ к сервисам

| Сервис        | URL                        |
| ------------- | -------------------------- |
| API (Swagger) | http://localhost:8000/docs |
| Adminer (БД)  | http://localhost:8080      |

---

### 4. Данные для подключения

#### PostgreSQL (Adminer)

* System: PostgreSQL
* Server: postgres
* User: postgres
* Password: postgres
* DB: db
