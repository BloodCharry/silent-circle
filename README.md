# Silent Circle - Telegram-only bot (collector)

This bot collects registration profiles and sends them to an admin for approval. After approval the bot prompts the user to upload a photo and write a short "about".

## Quick steps to run locally

1. Install Python 3.11 and pip.
2. Create virtualenv and activate:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill `BOT_TOKEN` and `ADMIN_CHAT_ID`.
5. Run the bot:
   ```bash
   python bot.py
   ```
6. In Telegram send `/start` to your bot and follow prompts.

## Docker (local)

1. Copy `.env.example` to `.env` and fill values.
2. Run:
   ```bash
   docker-compose up --build -d
   ```

## Notes
- This project uses long polling (suitable for local/testing). For production (Amvera/other PaaS) you may need webhook mode.
- Database: SQLite (./data/silentcircle.db). For production switch to PostgreSQL.
