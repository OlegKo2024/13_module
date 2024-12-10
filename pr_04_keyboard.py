from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import dotenv
import os

dotenv.load_dotenv()
api = os.getenv("BOT_TOKEN")
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')

kb = ReplyKeyboardMarkup(
    keyboard=[
        [button1, button2],  # Первый ряд
    ],
    resize_keyboard=True,)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(Command("start"))
async def start_com(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message(F.text == 'Рассчитать')
async def set_age(message: Message, state: FSMContext):
    await message.answer('Введите свой возраст, г: ')
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост, см: ')
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес, кг: ')
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def set_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_norm = 10 * int(data['weight']) + 6.5 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий (ккал) в сутки: {calories_norm}')
    print(f'Ваша норма калорий (ккал) в сутки: {calories_norm}')
    await state.clear()

@dp.message()
async def any_messages(message: Message):
    await message.reply('Введите команду /start, чтобы начать общение.')


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
