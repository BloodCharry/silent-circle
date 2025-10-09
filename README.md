# Silent Circle (черновой вариант)

Silent Circle — Telegram‑сервис для деловых знакомств интровертов.  
Он помогает предпринимателям, исследователям, студентам и специалистам находить полезные контакты в комфортной форме, без давления и спама.

##  Основные возможности
- Минималистичный Telegram‑бот:
  - приветствие и навигация;
  - уведомления о статусе анкеты и новых знакомствах;
  - обратная связь с администратором.
- Telegram Mini App:
  - регистрация и анкета с модерацией;
  - личный кабинет (профиль, интересы, фото);
  - еженедельный подбор собеседника и создание чата;
  - система подписки (2 бесплатных знакомства, далее платно).

## Архитектура
- **Backend**: FastAPI + aiogram, PostgreSQL, Redis, Celery/APScheduler
- **Frontend (Mini App)**: React + TypeScript, Telegram WebApp SDK
- **DevOps**: Docker, Nginx/Traefik, GitHub Actions, Sentry, Prometheus

Подробнее см. [docs/architecture.md](docs/architecture.md).

## Структура проекта

    silent-circle/

      ├── backend/ # FastAPI + aiogram

      ├── frontend/ # React + TS Mini App

      ├── devops/ # Docker, CI/CD, конфиги

      └── docs/ # документация

## Локальный запуск
### Требования
- Python 3.11+
- Node.js 18+
- Docker + Docker Compose

### Backend
```bash
cd backend
pip install poetry
poetry install
poetry run uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker Compose (всё вместе)
```bash
docker-compose -f devops/compose/docker-compose.dev.yml up --build
```

## Тестирование
```bash
pytest
```