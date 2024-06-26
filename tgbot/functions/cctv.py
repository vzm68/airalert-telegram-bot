import cv2

from tgbot.config import load_config

import logging

logger = logging.getLogger(__name__)

rtsp_url = load_config(".env").tg_bot.rtsp_url


def capture_rtsp_screenshot(output_file="yard.png"):
    # Open RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        logger.warning(f"Error: Unable to open RTSP stream")
        return

    # Read a frame from the stream
    ret, frame = cap.read()

    if ret:
        # Save the frame as an image
        cv2.imwrite(output_file, frame)
        logger.info(f"Screenshot saved to {output_file}")
    else:
        logger.warning("Error: Unable to capture a frame from the RTSP stream")
    cap.release()