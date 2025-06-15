import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

# Загружаем токен из переменных окружения
BOT_TOKEN = os.getenv(7647217847:AAFzmJ6NSMUEZyKtlHkWgkcxHSp8oYZg-0o)

# Проверка на наличие токена
if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

# Настройки логгера
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Сәлем! 🤖 Мен жұмыс істеп тұрмын!")

# Регистрируем роутер
dp.include_router(router)

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
