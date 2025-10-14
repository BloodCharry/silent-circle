import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.api.v1 import users, applications
from app.core.config import settings


TESTING = os.environ.get("TESTING") == "1"

if not TESTING:
    from dotenv import load_dotenv

    load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if TESTING:
        logging.info("Silent Circle backend started (TEST).")
        yield
        logging.info("Silent Circle backend stopped (TEST).")
    else:
        import asyncio
        from app.db.session import init_engine
        from aiogram import Bot, Dispatcher
        from aiogram.types import Message
        from aiogram.filters import Command
        from aiogram.enums import ParseMode
        from aiogram.client.default import DefaultBotProperties

        API_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()

        @dp.message(Command("start"))
        async def cmd_start(message: Message) -> None:
            await message.answer("Привет! Это Silent Circle.\nНажми кнопку ниже, чтобы перейти в приложение.")

        async def start_bot() -> None:
            logging.info("Starting Telegram bot...")
            await dp.start_polling(bot)

        # --- startup ---
        init_engine()
        asyncio.create_task(start_bot())
        logging.info("Silent Circle backend started.")

        try:
            yield
        finally:
            # --- shutdown ---
            await bot.session.close()
            logging.info("Silent Circle backend stopped.")


app = FastAPI(title="Silent Circle API", version="0.1.0", lifespan=lifespan)

# Роутеры
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["users"])
app.include_router(applications.router, prefix=f"{settings.API_V1_PREFIX}/applications", tags=["applications"])


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
