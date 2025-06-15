
import os
import re
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text:
        phone_pattern = re.compile(r"(?:(?:\+|8)?7)[\s\-]?(\d{3})[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})")
        phones = phone_pattern.findall(message.text)
        if phones:
            phones = ["+7" + "".join(phone) for phone in phones]
            await message.answer("\n".join(phones))
        else:
            await message.answer("Телефонный номер не найден.")
    else:
        await message.answer("Отправь текстовое сообщение.")

async def on_startup(bot: Bot) -> None:
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await bot.set_webhook(webhook_url)

async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()

def main():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot, on_startup=on_startup, on_shutdown=on_shutdown)
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

if __name__ == "__main__":
    main()
