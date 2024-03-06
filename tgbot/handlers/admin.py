from aiogram import Dispatcher, Bot
from aiogram.types import Message
from tgbot.config import load_config

from tgbot.functions.status import get_status

admin_ids = load_config(".env").tg_bot.admin_ids
chats_id = load_config(".env").tg_bot.chats


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def get_system_status(message: Message):
    await message.answer(text=get_status())


async def bot_notification(bot: Bot):
    for id in admin_ids:
        await bot.send_message(chat_id=id, text="🎯 Відбувся запуск бота")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(get_system_status, commands=["system"], is_admin=True)