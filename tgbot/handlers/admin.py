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
    try:
        with open("updates.txt", "r") as updates:
            if len(updates) > 7:
                for chat in chats_id:
                    await bot.send_message(chat_id=chat, text=updates.read())
                with open("updates.txt", "w") as clean:
                    pass
            else:
                pass
    except FileNotFoundError as err:
        for id in admin_ids:
            await bot.send_message(chat_id=id, text=err)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)