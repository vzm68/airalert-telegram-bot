from aiogram import Dispatcher
from aiogram.types import Message


async def user_start(message: Message):  # Temp command for test, i don't need it now
    await message.reply(f"Привіт, {message.from_user.first_name}!\n\n"
                        f"Я просто бот, нажаль, наразі я не виконую ніякої функції у цьому чаті.")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
