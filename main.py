import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F

TOKEN = '7338928947:AAF1UYcF9ZLL7l-Iczo4YF_zFATORBvAXb0'
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

buttons_labels = ["Оставить отзыв", "Сделать предложение", "Купить радиооборудование", "Стать дилером", "Задать вопрос", "Сервисный центр", "Тех.поддержка"]
buttons_comand = ["review", "makeOffer", "buy", "dealer", "question", "service", "support"]
buttons_list = {""}

# async def set_default_commands(dp):
#     await dp.bot.set_my_commands([
#         types.BotCommand(buttons_comand[0], buttons_labels[0]),
#         types.BotCommand(buttons_comand[1], buttons_labels[1]),
#         types.BotCommand(buttons_comand[2], buttons_labels[2]),
#         types.BotCommand(buttons_comand[3], buttons_labels[3]),
#         types.BotCommand(buttons_comand[4], buttons_labels[4]),
#     ])

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text=buttons_labels[0]),
        types.KeyboardButton(text=buttons_labels[1])
    )
    builder.row(types.KeyboardButton(
        text=buttons_labels[2])
    )
    builder.row(
        types.KeyboardButton(text=buttons_labels[3]),
        types.KeyboardButton(text=buttons_labels[4])
    )
    builder.row(
        types.KeyboardButton(text=buttons_labels[5]),
        types.KeyboardButton(text=buttons_labels[6])
    )
    await message.answer(
        "Привет, это бот Терек Радио! Выбирай в меню управления дальнешее дейсвие ⬇️",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.lower() == buttons_labels[0].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[0])

@dp.message(F.text.lower() == buttons_labels[1].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[1])
@dp.message(F.text.lower() == buttons_labels[2].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[2])
@dp.message(F.text.lower() == buttons_labels[3].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[3])
@dp.message(F.text.lower() == buttons_labels[4].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[4])
@dp.message(F.text.lower() == buttons_labels[5].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[5])
@dp.message(F.text.lower() == buttons_labels[6].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[6])

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())