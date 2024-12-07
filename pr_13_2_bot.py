from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
import asyncio
import dotenv
import os

dotenv.load_dotenv()
api = os.getenv("BOT_TOKEN")
bot = Bot(token=api)
storage = MemoryStorage()
router = Router()
dp = Dispatcher(storage=storage)
dp.include_router(router)


@router.message(Command("start"))
async def start_com(message: Message):
    print('Привет! Я бот помогающий твоему здоровью.')
    # await message.reply('Получена команда: ' + message.text)


@router.message(F.text.in_(['Urban', 'ff']))
async def urban_messages(message: Message):
    print('Urban message:', message.text)
    # await message.reply('Получено кодовое сообщение: ' + message.text)


@router.message()
async def any_messages(message: Message):
    print('Введите команду /start, чтобы начать общение.')
    # await message.reply('Получено сообщение: ' + message.text)


async def main():
    print("Updates were skipped successfully.")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

