from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import re
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message()
async def handle_phone(message: Message):
    phone = message.text.strip()
    digits = re.sub(r"\D", "", phone)
    if 9 < len(digits) <= 15:
        wa_link = f"https://wa.me/{digits}"
        await message.answer(f"<b>Ваш WhatsApp:</b> <a href='{wa_link}'>{wa_link}</a>")
    else:
        await message.answer("Пожалуйста, отправьте корректный номер телефона.")

async def on_startup(app):
    await bot.set_webhook(os.getenv("WEBHOOK_URL"))

def create_app():
    app = web.Application()
    dp.startup.register(on_startup)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")
    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, port=5000)
