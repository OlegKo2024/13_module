from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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

button_calc = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_func = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb = ReplyKeyboardMarkup(
    keyboard=[
        [button1, button2],
    ],
    resize_keyboard=True,
)

kb_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_calc, button_func]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(Command("start"))
async def start_com(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message(F.text == 'Рассчитать')
async def main_menu(message: Message):
    await message.answer('Выберите опцию', reply_markup=kb_menu)


@dp.callback_query(F.data == 'formulas')
async def inst(call):
    message_text = (
        'Формула Миффлина-Сан Жеора:\n'
        '- для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
        '- для женщин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161'
    )
    await call.message.answer(message_text)
    await call.answer()


@dp.callback_query(F.data == 'calories')
async def set_age(call, state: FSMContext):
    await call.message.answer('Введите свой возраст, г: ')
    await state.set_state(UserState.age)
    await call.answer()


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
    await message.answer(f'Ваша норма калорий (кал) в сутки: {calories_norm}')
    print(f'Ваша норма калорий (ккал) в сутки: {calories_norm}')
    await state.clear()


@dp.message()
async def any_messages(message: Message):
    await message.reply('Введите команду /start, чтобы начать общение.')


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
