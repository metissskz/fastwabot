from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from fastapi import FastAPI, Request
import re
import os

TOKEN = os.getenv("BOT_TOKEN") or "ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
app = FastAPI()

def clean_number(phone: str) -> str:
    return re.sub(r"[^\d+]", "", phone)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("📲 Отправь номер телефона, и я сгенерирую ссылку wa.me для WhatsApp.")

@dp.message_handler()
async def handle_phone(message: types.Message):
    number = clean_number(message.text)
    if number.startswith("+"):
        number = number[1:]
    if number.isdigit():
        link = f"https://wa.me/{number}"
        await message.reply(f"👉 [Перейти в WhatsApp]({link})", parse_mode="Markdown")
    else:
        await message.reply("⚠️ Пожалуйста, отправь корректный номер телефона.")

@app.post("/webhook")
async def process_webhook(request: Request):
    body = await request.json()
    update = types.Update(**body)
    await dp.process_update(update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "OK", "message": "Telegram WA Bot running"}
