from aiogram import Dispatcher, Bot
from aiogram.types import Message
from tgbot.config import load_config

admin_ids = load_config(".env").tg_bot.admin_ids
chats_id = load_config(".env").tg_bot.chats


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def bot_notification(bot: Bot):
    for id in admin_ids:
        await bot.send_message(chat_id=id, text="🎯 Відбувся запуск бота")


async def update_notify(bot: Bot):
    new_updates = """Last updates:\n\n
                    ▪️ Reduced time for checking the status of air-alarms to 15 sec\n
                    ▪️ Other changes"""
    old_updates = ""
    if new_updates != old_updates:
        for chat in chats_id:
            await bot.send_message(chat_id=chat, text=new_updates)
    else:
        pass


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
