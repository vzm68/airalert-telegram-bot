from aiogram import Dispatcher, Bot
from aiogram.types import Message, InputFile, ChatActions
from tgbot.handlers.daily import get_weather_data, get_daily_news
from tgbot.functions.cctv import capture_rtsp_screenshot
from tgbot.functions.crypto import crypto
from tgbot.functions.tuya_devices import tuya_sensors_info

import time
from random import randint
import g4f


async def user_start(message: Message):  # Temp command for test, i don't need it now
    await message.reply(f"Привіт, {message.from_user.first_name}!\n\n"
                        f"Я просто бот, нажаль, наразі я не виконую ніякої функції у цьому чаті.")


conversation_history = {}  # According to ask_gpt and clear_answers functions

users_info = {}  # collection of users with total liquid accumulated


async def get_yard_img(message: Message):
    try:
        capture_rtsp_screenshot()
        img = InputFile("yard.png")
        await message.answer_chat_action(action=ChatActions.UPLOAD_PHOTO)
        await message.reply_photo(photo=img)
    except Exception as err:
        await message.answer(text=str(err))


async def get_weather(message: Message):
    await message.reply(text=get_weather_data())


async def cum_joke(message: Message):
    global users_info

    user_name = message.from_user.first_name

    ending_letters = ''

    if user_name in users_info:
        users_info[user_name]['num'] += randint(1, 250)
        users_info[user_name]['last_call_time'] = time.time()
        users_info[user_name]['call_count'] += 1
    else:
        users_info[user_name] = {
            'num': randint(1, 250),
            'last_call_time': time.time(),
            'call_count': 1
        }

    if users_info[user_name]['call_count'] < 4:
        ending_letters = 'ння'
    else:
        ending_letters = 'нь'

    await message.answer(text=f"Видача <b>CUM</b> 💦💦💦 на лице <b>{user_name}</b>.\n\n"
                              f"Кількість отриманих мл = <b>{users_info[user_name]['num']}</b>🚰 за "
                              f"<b>{users_info[user_name]['call_count']}</b> закінче{ending_letters}✊")


async def news(message: Message):
    await message.answer(text=get_daily_news())


def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history


async def clear_answers(message: Message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.answer(f"Історія пов'язаних діалогів {message.from_user.first_name} з чат-ботом очищена.")
    await message.delete()


async def ask_gpt(message: Message):
    user_id = message.from_user.id
    user_input = message.reply_to_message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_input})
    conversation_history[user_id] = trim_history(conversation_history[user_id])

    chat_history = conversation_history[user_id]

    try:
        await message.answer_chat_action(ChatActions.TYPING)
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_35_turbo,
            messages=chat_history,
            provider=g4f.Provider.Liaobots,
        )
        chat_gpt_response = response
    except Exception as e:
        print(f"{g4f.Provider.Liaobots.__name__}:", e)
        chat_gpt_response = f"Виникла помилка під час обробки запиту: \n\n" \
                            f"<code>{e}</code>"

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    if message.reply_to_message.text:
        await message.reply_to_message.reply(chat_gpt_response)


async def get_crypto_price(message: Message):
    await message.answer(text=crypto())


async def get_tuya_sensors_info(message: Message):
    await message.answer(text=tuya_sensors_info())


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_weather, commands=["weather"])
    dp.register_message_handler(get_yard_img, commands=["cam1"])
    dp.register_message_handler(cum_joke, commands=["cum"])
    dp.register_message_handler(news, commands=["news"])
    dp.register_message_handler(ask_gpt, commands=["ask"])
    dp.register_message_handler(clear_answers, commands=["clear"])
    dp.register_message_handler(get_crypto_price, commands=["price"])
    dp.register_message_handler(get_tuya_sensors_info, commands=["sensors"])
