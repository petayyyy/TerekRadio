import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import filters
from aiogram.fsm.context import FSMContext
# from aiogram.dispatcher import FSMContext

from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = '7338928947:AAF1UYcF9ZLL7l-Iczo4YF_zFATORBvAXb0'
ADMIN_ID = '414231719'  # Замените на ID администратора
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

# Команда для ответа пользователю
class SupportState:
    awaiting_response = 0

# # Хэндлер на команду /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     kb = [
#         [types.KeyboardButton(text="С пюрешкой")],
#         [types.KeyboardButton(text="Без пюрешки")]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True,
#         input_field_placeholder="Выберите способ подачи"
#     )
#     await message.answer(f"Здравствуйте {message.from_user.full_name} Вас приветствует тех поддерка команды Терек Радио", reply_markup=keyboard)

@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Задать вопрос", request_location=True),
        types.KeyboardButton(text="Оставить отзыв", request_contact=True)
    )
    builder.row(
        types.KeyboardButton(text="Сделать предложение", request_location=True),
        types.KeyboardButton(text="Тех.поддержка", request_contact=True)
    )
    # ... второй из одной ...
    builder.row(types.KeyboardButton(
        text="Купить радиооборудование",
        request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    builder.row(
        types.KeyboardButton(text="Стать дилером", request_location=True),
        types.KeyboardButton(text="Сервисный центр", request_contact=True)
    )
    
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Добро пожаловать в техподдержку! Напишите свой вопрос.")

@dp.message(filters.Text & ~filters.Command())
async def send_to_admin(message: types.Message):
    # Ретранслируем сообщение администратору
    await bot.send_message(ADMIN_ID, f"Сообщение от (ID: {message.from_user.id}):\n\n{message.text}")
    await message.reply("Ваше сообщение отправлено администратору. Ожидайте ответа.")

@dp.message(Command("respond")", state='*')
async def cmd_respond(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.reply("Вы не являетесь администратором.")
        return
    
    await state.set_state(SupportState.awaiting_response)
    await message.reply("Введите сообщение для пользователя (через ID):")

@dp.message(state=SupportState.awaiting_response)
async def process_response(message: types.Message, state: FSMContext):
    # Разделяем ID и сообщение в формате "ID: сообщение"
    try:
        user_id, response_text = message.text.split(':', 1)
        user_id = int(user_id.strip())
        response_text = response_text.strip()

        await bot.send_message(user_id, f"Ответ от администрации:\n\n{response_text}")
        await message.reply(f"Ответ отправлен пользователю с ID: {user_id}")
    except ValueError:
        await message.reply("Некорректный формат. Используйте формат 'ID: сообщение'")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

    await state.finish()

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())