import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_CHANNEL_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def send_telegram(message):
    """
    Send a Telegram message to both personal chat and channel.
    Retries until successful.
    """
    targets = [TELEGRAM_CHAT_ID, TELEGRAM_CHANNEL_ID]

    for chat_id in targets:
        success = False
        while not success:
            try:
                payload = {"chat_id": chat_id, "text": message}
                response = requests.post(BASE_URL + "sendMessage", data=payload)
                if response.status_code == 200:
                    success = True
                else:
                    print(f"Telegram send to {chat_id} failed, retrying...")
                    time.sleep(2)
            except Exception as e:
                print(f"Telegram send exception for {chat_id}:", e)
                time.sleep(2)
