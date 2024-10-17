import logging
from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram import Router
from aiogram.utils import executor

API_TOKEN = '7338928947:AAF1UYcF9ZLL7l-Iczo4YF_zFATORBvAXb0'  # Замените на токен вашего бота
ADMIN_ID = '414231719'  # Замените на ID администратора

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage)

# Команда для ответа пользователю
class SupportState:
    awaiting_response = 0

@dp.message(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Добро пожаловать в техподдержку! Напишите свой вопрос.")

@dp.message(filters.Text & ~filters.Command())
async def send_to_admin(message: types.Message):
    # Ретранслируем сообщение администратору
    await bot.send_message(ADMIN_ID, f"Сообщение от (ID: {message.from_user.id}):\n\n{message.text}")
    await message.reply("Ваше сообщение отправлено администратору. Ожидайте ответа.")

@dp.message(commands=['respond'], state='*')
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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
