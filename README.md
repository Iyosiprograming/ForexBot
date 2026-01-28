# ForexBot MVP

A simple and lightweight Forex trading bot using **MetaTrader5**, designed for **EMA crossover strategy** with safe trade management and Telegram notifications.

---

## Key Features

- **EMA Crossover Signals** – Fast EMA and Slow EMA strategy for automated entries  
- **Safe Trade Execution** – Automatically closes opposite trades before opening new ones  
- **Stop Loss & Take Profit** – Pre-set SL and TP for every trade  
- **Trailing Stop Loss** – Moves SL to lock in profits  
- **Telegram Notifications** – Get instant alerts for every executed trade  

---

## Requirements

Python 3.8+ and the following libraries:

```

MetaTrader5
pandas
numpy
requests

````

Install all dependencies with:

```bash
pip install -r requirements.txt
````

---

## Setup

1. Open `config.py` and update your MT5 account and trading settings:

```python
MT5_Login = 123456
MT5_Password = "password"
MT5_Server = "Broker-Server"

Trade_Symbol = "EURUSDm"
Lot_Size = 0.01
Stop_Loss = 100      # points
Take_Profit = 200    # points

EMA_FAST = 10
EMA_SLOW = 20

# Telegram notifications
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
```

2. Make sure **MetaTrader5 desktop** is running and logged in.
3. Ensure your symbol is visible in Market Watch.
4. Enable **Algo Trading** in MT5.

---

## Running the Bot

```bash
python main.py
```

The bot will:

* Check EMA crossover signals every M1 candle
* Open/close trades safely
* Automatically update trailing Stop Loss
* Send Telegram alerts for all trade actions

---

## Folder Structure

```
ForexBot/
├── main.py
├── logic.py
├── trade_excuter.py
├── mt5_connect.py
├── config.py
├── telegram.py
├── requirements.txt
└── __pycache__/
```

---

## Notes

* **Demo First:** Always test on demo accounts before going live.
* **Points Not Pips:** SL and TP are measured in points.
* **Lightweight & MVP:** Minimal setup, easy to extend.

