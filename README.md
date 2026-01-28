# 📈ForexBot MVP

A simple Forex trading bot using MetaTrader5 and EMA crossover strategy. Sends trade alerts to Telegram.

---

## Features

- EMA crossover signals (fast and slow EMA)  
- Safe trade execution (closes opposite trades before opening new ones)  
- Stop Loss and Take Profit for every trade  
- Trailing Stop Loss  
- Telegram notifications to your chat and channel  

---

## Requirements

- Python 3.8+  
- Libraries: `MetaTrader5`, `pandas`, `numpy`, `requests`, `python-dotenv`  

Install dependencies:

```bash
pip install -r requirements.txt
````

---

## Setup

1. Create a `.env` file with your credentials:

```
MT5_LOGIN=123456
MT5_PASSWORD=yourpassword
MT5_SERVER=Broker-Server

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=@yourusername
TELEGRAM_CHANNEL_ID=@YourChannelUsername
```

2. Open MetaTrader5 and ensure your symbol is visible.
3. Enable Algo Trading in MT5.

---

## Running the Bot

```bash
python main.py
```

The bot will:

* Check EMA signals every 1-minute candle
* Open and close trades safely
* Update trailing Stop Loss
* Send Telegram notifications for every trade

---

## Folder Structure

```
ForexBot/
├── config.py
├── .env
├── main.py
├── logic.py
├── trade_excute.py
├── mt5_connect.py
├── telegram.py
├── README.md
├── requirements.txt
└── __pycache__/
```

---

## Notes

* Test on demo accounts first.
* Stop Loss and Take Profit are measured in points.
* Lightweight and easy to extend.
