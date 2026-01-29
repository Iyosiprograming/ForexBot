import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def send_telegram(message, retries=3, delay=2):
    """
    Send a Telegram message to the channel only.
    Will retry a few times if it fails, then give up.
    """
    if not TELEGRAM_CHANNEL_ID:
        return

    for attempt in range(1, retries + 1):
        try:
            payload = {"chat_id": TELEGRAM_CHANNEL_ID, "text": message}
            response = requests.post(BASE_URL + "sendMessage", data=payload, timeout=5)
            if response.status_code == 200:
                break
            else:
                print(f"Telegram send failed ({response.status_code}) attempt {attempt}")
        except Exception as e:
            print(f"Telegram exception: {e} attempt {attempt}")
        time.sleep(delay)
