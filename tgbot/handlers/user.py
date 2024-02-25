from aiogram import Dispatcher, Bot
from aiogram.types import Message, InputFile, ChatActions
from tgbot.handlers.daily import get_weather_data
from tgbot.config import load_config

import cv2


async def user_start(message: Message):  # Temp command for test, i don't need it now
    await message.reply(f"Привіт, {message.from_user.first_name}!\n\n"
                        f"Я просто бот, нажаль, наразі я не виконую ніякої функції у цьому чаті.")


def capture_rtsp_screenshot(rtsp_url, output_file="yard.png"):
    # Open RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"Error: Unable to open RTSP stream at {rtsp_url}")
        return

    # Read a frame from the stream
    ret, frame = cap.read()

    if ret:
        # Save the frame as an image
        cv2.imwrite(output_file, frame)
        print(f"Screenshot saved to {output_file}")
    else:
        print("Error: Unable to capture a frame from the RTSP stream")
    cap.release()


rtsp_url = load_config(".env").tg_bot.rtsp_url


async def get_yard_img(message: Message):
    capture_rtsp_screenshot(rtsp_url)
    img = InputFile("yard.png")
    await message.answer_chat_action(action=ChatActions.UPLOAD_PHOTO)
    await message.reply_photo(photo=img)


async def get_weather(message: Message):
    await message.reply(text=get_weather_data())


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_weather, commands=["weather"])
    dp.register_message_handler(get_yard_img, commands=["cam1"])
