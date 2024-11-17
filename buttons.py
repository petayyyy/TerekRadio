from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove
from aiogram import F
from  configs import *
from sheetEditor import *

buttons_labels = ["Оставить отзыв", "Сделать предложение", "Купить радиооборудование", "Стать дилером", "Задать вопрос", "Сервисный центр", "Тех.поддержка"]
buttons_comand = ["review", "makeOffer", "buy", "dealer", "question", "service", "support"]
buttons_list = {""}

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

EmptyBut = ReplyKeyboardBuilder()

ClearBut = ReplyKeyboardRemove()


# admins buttons
adminButInLine = InlineKeyboardBuilder()
adminButInLine.add(types.InlineKeyboardButton(
    text="Начать писать ответ",
    callback_data="answerM")
)

# service buttons
servBut = ReplyKeyboardBuilder()
servBut.row(
    types.KeyboardButton(text="Нет, помогло"),
    types.KeyboardButton(text="Все ещё остались вопросы")
)

servHBut = ReplyKeyboardBuilder()
servHBut.row(
    types.KeyboardButton(text="Помогло")
)

# questions
questionsBuld = [
    [
    types.InlineKeyboardButton(text="Ответ был полезен", callback_data="answerG"),
    types.InlineKeyboardButton(text="Уточните ответ", callback_data="answerB1"),
    types.InlineKeyboardButton(text="Задать ещё вопрос", callback_data="answerB2")
    ]
]
questionsBut = types.InlineKeyboardMarkup(inline_keyboard=questionsBuld)

questionsAdminBut = InlineKeyboardBuilder()
questionsAdminBut.add(types.InlineKeyboardButton(
    text="Начать писать ответ, на дополненый вопрос",
    callback_data="answerM")
)