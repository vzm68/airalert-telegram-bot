from aiogram import Dispatcher, Bot
from aiogram.types import Message, InputFile, ChatActions
from tgbot.handlers.daily import get_weather_data, get_daily_news
from tgbot.functions.cctv import capture_rtsp_screenshot, capture_rtsp_video
from tgbot.functions.crypto import crypto, index_price
from tgbot.functions.tuya_devices import tuya_sensors_info
from tgbot.functions.fun import martingale

import logging

logger = logging.getLogger(__name__)

import time
from random import randint, uniform
import g4f


async def user_start(message: Message):  # Temp command for test, i don't need it now
    await message.reply(f"Привіт, {message.from_user.first_name}!\n\n"
                        f"Я просто бот, нажаль, наразі я не виконую ніякої функції у цьому чаті.")


conversation_history = {}  # According to ask_gpt and clear_answers functions

users_info = {}  # collection of users with total liquid accumulated


async def get_yard_img(message: Message):
    try:
        await capture_rtsp_screenshot()
        img = InputFile("yard.png")
        await message.answer_chat_action(action=ChatActions.UPLOAD_PHOTO)
        await message.reply_photo(photo=img)
        logger.info(f"Cam1 photo was sent to {message.from_user.full_name}/{message.from_user.id}")
        # os.remove("yard.png")
    except Exception as err:
        await message.answer(text=str(err))
        logger.error(f"Problem with send RTSP capture: <code>{err}</code>")


async def get_yard_vid(message: Message):
    try:
        await capture_rtsp_video()
        mp4 = InputFile("yard.mp4")
        await message.answer_chat_action(action=ChatActions.UPLOAD_VIDEO)
        await message.reply_video(video=mp4)
        logger.info(f"Cam1 video was sent to {message.from_user.full_name}/{message.from_user.id}")
        # os.remove("yard.mp4")
    except Exception as err:
        await message.answer(text=str(err))
        logger.error(f"Problem with send RTSP video: <code>{err}</code>")


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


# This func should be deleted or changed to other in soon updates
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
    price = await crypto()
    await message.answer(text=price)
    logger.info(f"Crypto price was sent to {message.from_user.full_name}/{message.from_user.id}")


async def get_index_price(message: Message):
    index = message.get_args().upper()
    price = await index_price(index)
    await message.reply(price)
    logger.info(f"{index} price was sent to {message.from_user.full_name}/{message.from_user.id}")


async def get_tuya_sensors_info(message: Message):
    await message.answer(text=tuya_sensors_info())
    logger.info(f"Tuya sensors info was sent to {message.from_user.full_name}/{message.from_user.id}")


async def get_martingale(message: Message):
    args = message.get_args().split()

    if len(args) == 0:
        rand_balance = randint(500, 100000)
        rand_bet = randint(1, 500)
        await message.reply(f"Ну да, {message.from_user.first_name}, треба ж потикати...\n"
                             f"Ладно, тобі рандомний баланс <code>{rand_balance}</code> гривні та початкова ставка буде <code>{rand_bet}</code>.\nБудеш винен.")
        await message.answer(martingale(rand_balance, rand_bet))

    else:
        try:
            balance = float(args[0])
            bet = float(args[1])
            if balance <= 100000000 and bet <= 100000000:
                await message.reply(martingale(balance, bet))
            else:
                xd = round(uniform(50, 6000), 2)
                await message.answer(f"""💥 Frontier вийшов з ладу.\n@{message.from_user.username}, вам доведеться заплатити заборгованість за використання надлишкових екзафлопс, у розмірі <b>{xd}$</b>. Майте на увазі, що борг віднесено до вашого облікового запису, що має ідентифікатор <code>{message.from_user.id}</code>. Будь які спроби піти від відповідальності будуть переслідуватись згідно місцевого законодавства.""")
        except TypeError:
            await message.reply("Отримано невірний тип данних. Все просто ж.. Вкажи баланс та початкову ставку.\n<code>/martingale 1000 10</code>")
        except IndexError:
            await message.reply("Відсутня необхідна кількість аргументів. Все просто ж.. Вкажи баланс та початкову ставку.\n<code>/martingale 1000 10</code>")
        except ValueError:
            await message.reply("Невірне значення аргументів. Все просто ж.. Вкажи баланс та початкову ставку.\n<code>/martingale 1000 10</code>")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_weather, commands=["weather"])
    dp.register_message_handler(get_yard_img, commands=["cam1"])
    dp.register_message_handler(get_yard_vid, commands=["cam1v"])
    dp.register_message_handler(cum_joke, commands=["cum"])
    dp.register_message_handler(news, commands=["news"])
    dp.register_message_handler(ask_gpt, commands=["ask"])
    dp.register_message_handler(clear_answers, commands=["clear"])
    dp.register_message_handler(get_crypto_price, commands=["price"])
    dp.register_message_handler(get_index_price, commands=["index"])
    dp.register_message_handler(get_tuya_sensors_info, commands=["sensors"])
    dp.register_message_handler(get_martingale, commands=["martingale"])