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
sh = SheetEditor()

lastState = 0
lastUserId = 0
messageAdminId = 0  

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Привет, это бот Терек Радио! Выбирай в меню управления дальнейшее действие ⬇️",
        reply_markup=HomeButton.as_markup(resize_keyboard=True),
    )
# Отзыв
@dp.message(F.text.lower() == buttons_labels[0].lower())
async def with_puree(message: types.Message):
    global lastState
    lastState = 1

    await message.answer(
        "Напишите и оправте отзыв в одном сообщении",
        reply_markup=ClearBut,
        parse_mode="MarkdownV2"
    )
# Предложение
@dp.message(F.text.lower() == buttons_labels[1].lower())
async def with_puree(message: types.Message):
    global lastState
    lastState = 8

    await message.answer(
        "Напишите и оправте предложение в одном сообщении",
        reply_markup=ClearBut,
        parse_mode="MarkdownV2"
    )

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
    print(len(sh.ReadDataDillers()))
    await message.answer(
        "Напишите Ваш аддрес для подбора \nдля Вас наиближайшего диллера в формате \nГород улица, пример \nг\. Москва ул\. Пионеров",
        reply_markup=ClearBut,
        parse_mode="MarkdownV2"
    )

# Вопрос
@dp.message(F.text.lower() == buttons_labels[4].lower())
async def with_puree(message: types.Message):
    global lastState
    lastState = 2

    await message.answer(
        "Напишите Ваш вопрос",
        reply_markup=ClearBut,
        parse_mode="MarkdownV2"
    )

#region Answers
@dp.callback_query(F.data == "answerM")
async def send_random_value(callback: types.CallbackQuery):
    lastState = 5
    await callback.message.answer("Пишите ответ")
    await bot.edit_message_reply_markup(
        chat_id=chatId,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
@dp.callback_query(F.data == "answerG")
async def send_random_value(callback: types.CallbackQuery):
    await bot.send_message(chatId,  text="Ответ устроил пользователя")
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        reply_markup=None
    )
    await callback.message.answer(
        "Были рады ответить на Ваш вопрос, пишите ещё!",
        reply_markup=HomeButton.as_markup(resize_keyboard=True),
    )

@dp.callback_query(F.data == "answerB1")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer( text="Ожидайте ответа тех. поддержки", 
        reply_markup=EmptyBut.as_markup(resize_keyboard=True)
    )
    await bot.send_message(chatId,  text="Ответ не устроил пользователя, разверните его", reply_markup= adminButInLine.as_markup())

@dp.callback_query(F.data == "answerB2")
async def send_random_value(callback: types.CallbackQuery):
    lastState = 6
    lastUserId = callback.message.from_user.id

    await callback.message.answer(
        "Дополните вопрос и оправте его в одном сообщении",
        reply_markup=ClearBut,
        parse_mode="MarkdownV2"
    )
#endregion

# Сервисный центр
#region SerCentr
@dp.message(F.text.lower() == buttons_labels[5].lower())
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Ссылку на ютуб канал Терек-Радио с инструкциями: https://youtube.com/@terek-radio?si=FWB7JgVCcBpp4Ws- . Остались еще вопросы?",
        reply_markup=servBut.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.lower() == "Все ещё остались вопросы".lower())
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Контакт СЦ: моб: 8 (988) 243-16-97",
        reply_markup=servHBut.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.lower() == "Помогло".lower())
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Отлично!",
        reply_markup=HomeButton.as_markup(resize_keyboard=True)
    )
@dp.message(F.text.lower() == "Нет, помогло".lower())
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Попробуйте задать вопрос, наша тех поддержка найдет ответ на любой интересующий Вас вопрос",
        reply_markup=HomeButton.as_markup(resize_keyboard=True)
    )
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
        print("Update sheet data")
@dp.message(Command("updateList"))
async def with_puree(message: types.Message):
    if (listUs.CheckIsAdmin(message)):
        print("Update sheet data")
@dp.message(Command("clearUser"))
async def with_puree(message: types.Message):
    if (listUs.CheckIsAdmin(message)):
        print("Clear user data")
#endregion 

@dp.message()
async def cmd_special_buttons(message: types.Message):
    global lastState, lastUserId
    idU = message.from_user.id
    if (lastState == 1):
        print("Rewies")
        await message.answer(
            "Ваш отзыв успешно создан",
            reply_markup=HomeButton.as_markup(resize_keyboard=True)
        )
        sh.SendReviews(message.from_user.id, message.from_user.full_name, message.text)
    elif (lastState == 2): 
        print("New Question")
        lastUserId = message.from_user.id
        await bot.send_message(chatId,  text=message.text, reply_markup= adminButInLine.as_markup())
        await message.answer( text="Ожидайте ответа тех. поддержки", 
            reply_markup=EmptyBut.as_markup(resize_keyboard=True)
        )
    elif (lastState == 5):
        await bot.send_message(lastUserId,  text=message.text, reply_markup=questionsBut)
    elif (lastState == 6):
        print("Update Question")
        lastUserId = message.from_user.id
        await bot.send_message(chatId,  text=message.text, reply_markup= questionsAdminBut.as_markup())
        await message.answer( text="Ожидайте ответа тех. поддержки", 
            reply_markup=EmptyBut.as_markup(resize_keyboard=True)
        )
    elif (lastState == 8):
        print("MakeOffer")
        await message.answer(
            "Ваше предложение успешно создано",
            reply_markup=HomeButton.as_markup(resize_keyboard=True)
        )
        sh.SendOffer(message.from_user.id, message.from_user.full_name, message.text)
    else:
        print("Error states")
    lastState = 0

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    # sh = SheetEditor()
    listUs = UserList()
    asyncio.run(main())