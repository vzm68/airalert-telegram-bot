import asyncio

import cv2
import time
from concurrent.futures import ThreadPoolExecutor

from tgbot.config import load_config

import logging

logger = logging.getLogger(__name__)

rtsp_url = load_config(".env").tg_bot.rtsp_url

executor = ThreadPoolExecutor()


def capture_rtsp_screenshot_sync(output_file="yard.png"):
    try:
        # Open RTSP stream
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            logging.warning("Unable to open RTSP stream.")
            return

        # Optionally skip frames to quickly get the latest
        for _ in range(5):  # Skip first 5 frames for speed, adjust as necessary
            cap.grab()

        # Read a frame from the stream
        ret, frame = cap.read()

        if ret:
            # Save the frame as an image
            cv2.imwrite(output_file, frame)
            logging.info(f"Screenshot saved to {output_file}")
        else:
            logging.warning("Error: Unable to capture a frame from the RTSP stream")

    except Exception as e:
        logging.error(f"An exception occurred: {e}")
    finally:
        # Always release the capture object
        cap.release()


def capture_rtsp_video_sync(output_video="yard.mp4", video_duration=10, fps=20):
    try:
        # Open RTSP stream
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            logging.warning("Unable to open RTSP stream")
            return

        # Get frame width and height
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define the codec and create VideoWriter object for video recording
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

        # Record video for the specified duration
        start_time = time.time()
        while (time.time() - start_time) < video_duration:
            ret, frame = cap.read()
            if ret:
                out.write(frame)  # Write the frame into the video file
            else:
                logging.warning("Error: Unable to capture a frame during video recording")
                break

        logging.info(f"Video saved to {output_video}")

    except Exception as e:
        logging.error(f"An exception occurred: {e}")
    finally:
        # Always release the capture object and video writer
        cap.release()
        out.release()


async def capture_rtsp_screenshot(output_file="yard.png"):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, capture_rtsp_screenshot_sync, output_file)


async def capture_rtsp_video(output_video="yard.mp4", video_duration=10, fps=20):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, capture_rtsp_video_sync, output_video)