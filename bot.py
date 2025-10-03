import logging
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import init_db, create_or_update_user, get_user_by_tg, update_user_by_tg, list_pending_users

from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID') or 0)

if not API_TOKEN:
    raise RuntimeError('BOT_TOKEN not set in environment')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Register(StatesGroup):
    name = State()
    status = State()
    status_meta = State()

class AboutState(StatesGroup):
    about = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await init_db()
    user = await get_user_by_tg(message.from_user.id)
    if user:
        state = user.get('state')
        if state == 'pending':
            await message.reply('Ваша анкета отправлена на модерацию. Ожидайте подтверждения.')
            return
        if state == 'approved':
            await message.reply('Ваша анкета одобрена. Отправьте фото или напишите о себе /about')
            return
    await message.reply('Привет! Давай заполним анкету.\nВведите ваше имя и фамилию:')
    await Register.name.set()

@dp.message_handler(state=Register.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await create_or_update_user(message.from_user.id, full_name=name, state='collecting')
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton('Студент'), KeyboardButton('Работник компании'))
    markup.add(KeyboardButton('Предприниматель'), KeyboardButton('Ученый/исследователь'))
    await message.reply('Выберите ваш статус:', reply_markup=markup)
    await Register.status.set()

@dp.message_handler(state=Register.status)
async def process_status(message: types.Message, state: FSMContext):
    status = message.text.strip()
    await update_user_by_tg(message.from_user.id, status=status)
    if status.lower().startswith('студент'):
        await message.reply('Укажите университет, курс и специальность через запятую (пример: МГУ, 2, Физика)')
    elif status.lower().startswith('работник'):
        await message.reply('Укажите компанию и должность через запятую (пример: Яндекс, Менеджер)')
    elif status.lower().startswith('предприниматель'):
        await message.reply('Укажите название компании и вашу роль через запятую (пример: SilentCircle LLC, Основатель)')
    else:
        await message.reply('Укажите место работы/учёбы и сферу исследований через запятую (пример: ИТМО, Машинное обучение)')
    await Register.status_meta.set()

@dp.message_handler(state=Register.status_meta)
async def process_status_meta(message: types.Message, state: FSMContext):
    meta_text = message.text.strip()
    try:
        meta = {'raw': meta_text}
        await update_user_by_tg(message.from_user.id, status_meta=json.dumps(meta), state='pending')
    except Exception as e:
        await message.reply('Ошибка при сохранении. Попробуйте снова.')
        await state.finish()
        return

    user = await get_user_by_tg(message.from_user.id)
    user_info = f"Анкета #{user['id']}\n{user['full_name']}\nСтатус: {user.get('status')}\nДоп: {meta_text}\nTelegram: @{message.from_user.username or 'не указан'} (id: {message.from_user.id})"
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton('Одобрить', callback_data=f'admin:approve:{message.from_user.id}'),
        InlineKeyboardButton('Отклонить', callback_data=f'admin:reject:{message.from_user.id}')
    )
    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(ADMIN_CHAT_ID, user_info, reply_markup=keyboard)
            await message.reply('Спасибо! Ваша анкета отправлена на модерацию. Ожидайте подтверждения.')
        except Exception as e:
            await message.reply('Не удалось уведомить администратора. Попробуйте позже.')
            logger.exception('Failed to notify admin')
    else:
        await message.reply('ADMIN_CHAT_ID не настроен, анкета сохранена в статусе pending.')

    await state.finish()

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('admin:'))
async def process_admin_callback(callback_query: types.CallbackQuery):
    code = callback_query.data
    parts = code.split(':')
    if len(parts) != 3:
        await callback_query.answer('Неверный callback', show_alert=True)
        return
    action = parts[1]
    try:
        tg_id = int(parts[2])
    except:
        await callback_query.answer('Неверный ID', show_alert=True)
        return
    if callback_query.from_user.id != ADMIN_CHAT_ID:
        await callback_query.answer('У вас нет прав', show_alert=True)
        return

    if action == 'approve':
        await update_user_by_tg(tg_id, state='approved')
        await callback_query.answer('Пользователь одобрен')
        try:
            await bot.send_message(tg_id, 'Ваша анкета одобрена! Пожалуйста, загрузите фотографию (просто отправьте фото) и напишите немного о себе командой /about')
        except Exception as e:
            logger.exception('Failed to send approval message to user')
        await callback_query.message.edit_text(f'Анкета {tg_id} одобрена')
    elif action == 'reject':
        await update_user_by_tg(tg_id, state='rejected')
        await callback_query.answer('Пользователь отклонён')
        try:
            await bot.send_message(tg_id, 'К сожалению, ваша анкета отклонена.')
        except Exception:
            pass
        await callback_query.message.edit_text(f'Анкета {tg_id} отклонена')
    else:
        await callback_query.answer('Неизвестное действие', show_alert=True)

@dp.message_handler(commands=['pending'])
async def cmd_pending(message: types.Message):
    if message.from_user.id != ADMIN_CHAT_ID:
        await message.reply('Доступно только админу')
        return
    pend = await list_pending_users()
    if not pend:
        await message.reply('Нет ожидающих анкет.')
        return
    text = 'Ожидающие анкеты:\n'
    for u in pend:
        text += f"#{u['id']} - {u['full_name']} (tg: {u['telegram_id']})\n"
    await message.reply(text)

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    user = await get_user_by_tg(message.from_user.id)
    if not user or user.get('state') != 'approved':
        await message.reply('Фото можно отправлять только после одобрения анкеты.')
        return
    file_id = message.photo[-1].file_id
    await update_user_by_tg(message.from_user.id, photo_file_id=file_id)
    await message.reply('Фото сохранено. Спасибо!')

@dp.message_handler(commands=['about'])
async def cmd_about(message: types.Message):
    user = await get_user_by_tg(message.from_user.id)
    if not user or user.get('state') != 'approved':
        await message.reply('Вы можете заполнить информацию о себе только после одобрения анкеты.')
        return
    await message.reply('Напишите несколько слов о себе (не более 1000 символов):')
    await AboutState.about.set()

@dp.message_handler(state=AboutState.about)
async def process_about(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if len(text) > 1000:
        await message.reply('Слишком длинный текст. Уменьшите до 1000 символов.')
        return
    await update_user_by_tg(message.from_user.id, about=text)
    await message.reply('Информация о себе сохранена.')
    await state.finish()

@dp.message_handler(commands=['profile'])
async def cmd_profile(message: types.Message):
    user = await get_user_by_tg(message.from_user.id)
    if not user:
        await message.reply('Профиль не найден. Напишите /start чтобы создать анкету.')
        return
    text = f"Профиль #{user['id']}\nИмя: {user.get('full_name')}\nСтатус: {user.get('status')}\nО себе: {user.get('about') or '(не заполнено)'}\nСостояние: {user.get('state')}"
    if user.get('photo_file_id'):
        await bot.send_photo(message.from_user.id, user.get('photo_file_id'), caption=text)
    else:
        await message.reply(text)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, skip_updates=True)
