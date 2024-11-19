import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
import sys
from configs import *
from sheetEditor import *
from buttons import HomeButton, EmptyBut, ClearBut, buttons_labels, buttons_comand, adminButInLine, servBut, servHBut, questionsBut, questionsAdminBut
from user import UserList

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Добрый день! Это бот Терек-Радио. Выберите в меню управления дальнейшее действие ⬇️",
        reply_markup=HomeButton.as_markup(resize_keyboard=True),
    )
# Отзыв
@dp.message(F.text.lower() == buttons_labels[0].lower())
async def with_puree(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=8)

# Предложение
@dp.message(F.text.lower() == buttons_labels[1].lower())
async def with_puree(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=9)


# Стать диллером
@dp.message(F.text.lower() == buttons_labels[3].lower())
async def with_puree(message: types.Message):
    await message.answer(
        "Напишите в отдел по работе с клиентами\nДенису Гайнитдинову на почту: dg@terek\-radio\.ru\nили позвоните по номеру телефона: 8 \(989\) 260\-15\-95",
        reply_markup=HomeButton.as_markup(resize_keyboard=True),
        parse_mode="MarkdownV2"
    )

# Купить
@dp.message(F.text.lower() == buttons_labels[2].lower())
async def with_puree(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=12)
#region Answers
# Вопрос
@dp.message(F.text.lower() == buttons_labels[4].lower())
async def with_puree(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=3)

@dp.callback_query(F.data == "answerM")
async def send_random_value(callback: types.CallbackQuery):
    await listUs.CheckAdmMessage(messageU=callback.message, state=92)

@dp.callback_query(F.data == "answerG")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
    await listUs.CheckMessage(messageU=callback.message, state=10)


@dp.callback_query(F.data == "answerB1")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
    await listUs.CheckMessage(messageU=callback.message, state=11)

@dp.callback_query(F.data == "answerB2")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
    await listUs.CheckMessage(messageU=callback.message, state=2)

# Тех. поддержка
@dp.message(F.text.lower() == buttons_labels[6].lower())
async def with_puree(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=3)


#endregion

# Сервисный центр
#region SerCentr
@dp.message(F.text.lower() == buttons_labels[5].lower())
async def cmd_special_buttons(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=4)
@dp.message(F.text.lower() == "Все ещё остались вопросы".lower())
async def cmd_special_buttons(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=5)
@dp.message(F.text.lower() == "Помогло".lower())
async def cmd_special_buttons(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=6)
@dp.message(F.text.lower() == "Вопросов больше нет".lower())
async def cmd_special_buttons(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=7)
#endregion

#region System
@dp.message(Command("kill"))
async def with_puree(message: types.Message):
    if (listUs.CheckIsAdmin(message)):
        await message.answer("Выключение бота")
        sys.exit(0)
@dp.message(Command("updateSheet"))
async def with_puree(message: types.Message):
    if (listUs.CheckIsAdmin(message)):
        await listUs.CheckAdmMessage(messageU=message, state=93)
        print("Update sheet data")
@dp.message(Command("updateList"))
async def with_puree(message: types.Message):
    if (listUs.CheckIsAdmin(message)):
        await listUs.CheckAdmMessage(messageU=message, state=93)
        print("Update sheet data")
@dp.message(Command("clearUser"))
async def with_puree(message: types.Message):
    if (listUs.CheckIsAdmin(message)):
        print("Clear user data")
@dp.message(Command("list"))
async def with_puree(message: types.Message):
    if (listUs.CheckIsAdmin(message)):
        msg = listUs.PrintData()
        print(msg)
        # await message.answer(
        #     msg,
        #     reply_markup=ClearBut,
        #     parse_mode="MarkdownV2"
        # )
#endregion 

#region Map
@dp.callback_query(F.data == "map1")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
    await listUs.CheckMessage(messageU=callback.message, state=13)
@dp.callback_query(F.data == "map2")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
    await listUs.CheckMessage(messageU=callback.message, state=14)
@dp.callback_query(F.data == "map3")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
    await listUs.CheckMessage(messageU=callback.message, state=15)
#endregion


@dp.message()
async def cmd_special_buttons(message: types.Message):
    await listUs.CheckMessage(messageU=message, state=1)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    listUs = UserList(botM=bot)
    asyncio.run(main())