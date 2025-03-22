import logging
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

user_data = {
    "last_hcg": None,
    "supplements": set(),
    "workouts_done": [],
    "weight_log": []
}

TRAINING_DAYS = {
    1: "🏋️ ВТОРНИК — Фулбади тренировка 1\nПресс, ноги, спина, грудь, плечи, руки",
    3: "🏋️ ЧЕТВЕРГ — Фулбади тренировка 2\nНемного выше объём, другая техника",
    5: "🏋️ СУББОТА — Лёгкий объем + памп\nПоддержание, восстановление"
}

SUPPLEMENTS = {
    "утро": ["D3", "Хром", "Ежовик", "Testobooster"],
    "день": ["Q10 + ALA", "Microbiome Booster"],
    "вечер": ["Омега-3", "Магний", "Цинк", "5-HTP"]
}

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет, Саня! Это твой бот:\n/today — тренировка\n/done — отметить\n/bady — чеклист\n/hcg — ХГЧ лог\n/weight XX.X — вес\n/log — история")

@dp.message_handler(commands=["today"])
async def today_plan(message: types.Message):
    weekday = datetime.now().weekday()
    plan = TRAINING_DAYS.get(weekday, "Сегодня нет тренировки — отдыхай!")
    await message.reply(plan)

@dp.message_handler(commands=["done"])
async def mark_done(message: types.Message):
    date_str = datetime.now().strftime("%Y-%m-%d")
    user_data["workouts_done"].append(date_str)
    await message.reply(f"Отметил! Тренировка за {date_str} записана.")

@dp.message_handler(commands=["bady"])
async def supplements_checklist(message: types.Message):
    response = "💊 <b>БАДы на сегодня:</b>\n"
    for time, supps in SUPPLEMENTS.items():
        response += f"🕒 <b>{time.capitalize()}:</b> " + ", ".join(supps) + "\n"
    await message.reply(response, parse_mode="HTML")

@dp.message_handler(commands=["hcg"])
async def hcg_check(message: types.Message):
    today = datetime.now().strftime("%Y-%m-%d")
    last = user_data["last_hcg"]
    reply = f"Последняя инъекция: {last or 'не зафиксирована'}\nСегодня: {today}\nЧтобы отметить — напиши /hcg_done"
    await message.reply(reply)

@dp.message_handler(commands=["hcg_done"])
async def mark_hcg(message: types.Message):
    today = datetime.now().strftime("%Y-%m-%d")
    user_data["last_hcg"] = today
    await message.reply(f"Инъекция ХГЧ за {today} записана.")

@dp.message_handler(commands=["log"])
async def show_log(message: types.Message):
    log = "📝 <b>Твоя история:</b>\n"
    log += f"📌 ХГЧ: {user_data['last_hcg'] or 'не указано'}\n"
    log += f"✅ Тренировки: {len(user_data['workouts_done'])}\n"
    log += f"⚖️ Весов в логе: {len(user_data['weight_log'])}"
    await message.reply(log, parse_mode="HTML")

@dp.message_handler(commands=["weight"])
async def log_weight(message: types.Message):
    try:
        weight = float(message.text.split()[1])
        user_data["weight_log"].append((datetime.now().strftime("%Y-%m-%d"), weight))
        await message.reply(f"Вес {weight} кг записан.")
    except:
        await message.reply("Формат: /weight 91.6")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)