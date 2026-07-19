# AI FAQ Assistant

AI FAQ Assistant — это учебный проект, демонстрирующий разработку AI Backend приложения на **FastAPI** с использованием современных практик Python-разработки.

На текущем этапе реализован базовый AI-чат с сохранением истории сообщений в PostgreSQL, потоковой (streaming) генерацией ответов и логированием использования токенов LLM.

Проект разрабатывается поэтапно. В дальнейшем планируется добавить Tool Calling, RAG, LangGraph и поддержку нескольких LLM-провайдеров.

---

# Возможности

- AI-чат
- Streaming ответов
- Сохранение истории диалогов
- Логирование использования токенов
- Dependency Injection
- Асинхронный стек
- PostgreSQL
- Docker Compose

---

# Технологии

- Python 3.13+
- FastAPI
- SQLAlchemy 2.x (Async)
- PostgreSQL
- asyncpg
- Pydantic v2
- OpenAI SDK *(планируется замена на Ollama на следующем этапе)*
- Docker
- Docker Compose

---

# Архитектура

Проект построен по принципам многослойной архитектуры (Layered Architecture) с использованием Dependency Injection.

```
HTTP Request
      │
      ▼
Controller
      │
      ▼
ChatService
      │
      ├────────► LLM Client
      │
      ▼
ConversationRepository
      │
      ▼
PostgreSQL
```

### Слои приложения

| Слой | Ответственность |
|------|-----------------|
| controllers | HTTP API |
| services | бизнес-логика |
| repository | работа с PostgreSQL |
| clients | работа с LLM |
| protocols | интерфейсы зависимостей |
| schemas | ORM модели SQLAlchemy |
| models | Pydantic модели |

---

# Структура проекта

```
.
├── app
│   ├── clients.py
│   ├── controllers.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── protocols.py
│   ├── repository.py
│   ├── schemas.py
│   └── services.py
│
├── routers
│   └── api_v1_router.py
│
├── settings
│   └── settings.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── main.py
└── .env
```

---

# Используемые архитектурные принципы

- SOLID
- DRY
- KISS
- Dependency Injection
- Repository Pattern
- Protocol-based interfaces (PEP 544)

---

# Поток обработки запроса

```
Client
    │
POST /chat
    │
    ▼
Controller
    │
    ▼
ChatService
    │
    ├── сохранить сообщение пользователя
    │
    ├── получить историю диалога
    │
    ├── отправить историю в LLM
    │
    ├── начать streaming ответа
    │
    ├── сохранить ответ модели
    │
    └── сохранить usage токенов
    │
    ▼
StreamingResponse
```

---

# База данных

## Conversation

Хранит информацию о диалоге.

## Message

Хранит:

- роль сообщения
- текст сообщения
- время создания
- prompt tokens
- completion tokens
- total tokens

---

# API

## POST

```
POST /api/v1/chat
```

### Request

```json
{
    "conversation_id": 1,
    "message": "Привет!"
}
```

или

```json
{
    "message": "Привет!"
}
```

Если conversation_id отсутствует, создается новый диалог.

---

### Response

Ответ возвращается потоково (`text/plain`).

Также в заголовке присутствует

```
X-Conversation-ID
```

который необходимо использовать при последующих запросах.

---

# Streaming

Ответ модели не ожидает полного завершения генерации.

Клиент начинает получать токены сразу после начала генерации.

```
Привет...

Чем...

могу...

помочь...
```

---

# Использование

## 1. Клонировать проект

```bash
git clone <repo>
```

---

## 2. Создать .env

```
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=ai_assistant
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

OPENAI_API_KEY=...

OPENAI_MODEL=gpt-4.1-mini
```

---

## 3. Запустить

```bash
docker compose up --build
```

---

## Swagger

```
http://localhost:8000/docs
```

---

# Следующие этапы

- переход на Ollama
- поддержка нескольких LLM
- Tool Calling
- RAG
- LangChain
- LangGraph
- Qdrant
- Redis
- Prometheus
- LangSmith

---

# Цель проекта

Проект создается как практическое руководство по разработке современных AI Backend приложений на Python.

Основная цель — пройти путь от простого AI-чата до production-ready AI Agent с использованием LangChain/LangGraph, RAG и современных архитектурных практик.