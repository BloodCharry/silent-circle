import asyncio
import logging
import os

from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv

load_dotenv()

# Settings
API_TOKEN: str = os.environ["API_TOKEN"]
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# FastAPI
app = FastAPI(title="Silent Circle API", version="0.1.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Aiogram Handlers
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Это Silent Circle.\n"
        "Нажми кнопку ниже, чтобы перейти в приложение."
    )
    # Здесь позже добавим кнопку "Перейти в Mini App"


# Запуск бота и API
async def start_bot():
    logging.info("Starting Telegram bot...")
    await dp.start_polling(bot)


@app.on_event("startup")
async def on_startup():
    # Запускаем бота в фоне
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    logging.info("Silent Circle backend started.")


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logging.info("Silent Circle backend stopped.")
