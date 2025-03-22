import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode

API_TOKEN = "7342845325:AAGsgT0hM6byu8J_uwbFhdhkakfao5BHiAg"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Команда /start
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет, Саня! Это твой бот:\n/today — тренировка\n/done — отметить\n/day — чеклист\n/hcg — ХГЧ лог\n/weight_XX.X — вес\n/log — история"
    )

# Команда /today
@dp.message(F.text == "/today")
async def cmd_today(message: types.Message):
    await message.answer("Сегодня тренировка 💪\n18:00 — зал!")

# Команда /done
@dp.message(F.text == "/done")
async def cmd_done(message: types.Message):
    await message.answer("Тренировка отмечена ✅")

# Команда /day
@dp.message(F.text == "/day")
async def cmd_day(message: types.Message):
    await message.answer("Чеклист: \n- БАДы принял?\n- Воды попил?\n- Утро началось правильно?")

# Команда /hcg
@dp.message(F.text == "/hcg")
async def cmd_hcg(message: types.Message):
    await message.answer("Последняя инъекция ХГЧ: 🧬\n(логика позже)")

# Команда /log
@dp.message(F.text == "/log")
async def cmd_log(message: types.Message):
    await message.answer("Вот твоя история тренировок 📊\n(запись позже)")

# Команда /weight_XX
@dp.message(F.text.startswith("/weight_"))
async def cmd_weight(message: types.Message):
    try:
        weight = message.text.split("_")[1]
        await message.answer(f"Вес {weight} кг записан ⚖️")
    except:
        await message.answer("Формат: /weight_91.6")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
