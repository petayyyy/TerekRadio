import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
import sys

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

HomeButton = ReplyKeyboardBuilder()
# метод row позволяет явным образом сформировать ряд
# из одной или нескольких кнопок. Например, первый ряд
# будет состоять из двух кнопок...
HomeButton.row(
    types.KeyboardButton(text=buttons_labels[0]),
    types.KeyboardButton(text=buttons_labels[1])
)
HomeButton.row(types.KeyboardButton(
    text=buttons_labels[2])
)
HomeButton.row(
    types.KeyboardButton(text=buttons_labels[3]),
    types.KeyboardButton(text=buttons_labels[4])
)
HomeButton.row(
    types.KeyboardButton(text=buttons_labels[5]),
    types.KeyboardButton(text=buttons_labels[6])
)


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
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Нет, помогло"),
        types.KeyboardButton(text="Все ещё остались вопросы")
    )
    await message.answer(
        "Ссылку на ютуб канал Терек-Радио с инструкциями: https://youtube.com/@terek-radio?si=FWB7JgVCcBpp4Ws- . Остались еще вопросы?",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.lower() == "Все ещё остались вопросы".lower())
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Помогло")
    )
    await message.answer(
        "Контакт СЦ: моб: 8 (988) 243-16-97",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.lower() == "Помогло".lower())
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Уря",
        reply_markup=HomeButton.as_markup(resize_keyboard=True),
    )
@dp.message(F.text.lower() == "Нет, помогло".lower())
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Уря",
        reply_markup=HomeButton.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.lower() == buttons_labels[6].lower())
async def with_puree(message: types.Message):
    await message.reply(buttons_labels[6])

@dp.message(Command("kill"))
async def with_puree(message: types.Message):
    await message.answer("Выключение бота")
    sys.exit(0)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())