
# 📈 ForexBot MVP

A simple Forex trading bot using MetaTrader5 and EMA crossover strategy. Sends trade alerts **only to the Telegram channel** `@ajjfklajfklajfkljkl`.

---

## Features

* EMA crossover signals (fast & slow EMA)
* Safe trade execution (closes opposite trades before opening new trades)
* Stop Loss and Take Profit
* Configurable trailing Stop Loss (activation, distance, step)
* Telegram notifications **only to the channel**

---

## Requirements

* Python 3.8+
* Libraries: `MetaTrader5`, `pandas`, `numpy`, `requests`, `python-dotenv`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

1. Create a `.env` file:

```
MT5_LOGIN=123456
MT5_PASSWORD=yourpassword
MT5_SERVER=Broker-Server

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@ajjfklajfklajfkljkl
```

2. Open MetaTrader5 and enable Algo Trading.
3. Ensure your trading symbol is visible in MT5.

> **Note:** Bot only sends alerts to the channel. Users can enhance it to add personal chat notifications.

---

## Config (`config.py`)

```python
Trade_Symbol = "EURUSDm"
Lot_Size = 0.01
Stop_Loss = 100        # pips
Take_Profit = 200      # pips
MAGIC = 123456
DEVIATION = 10

USE_TRAILING_SL = True
TRAIL_START_PIPS = 50
TRAIL_DISTANCE_PIPS = 100
TRAIL_STEP_PIPS = 10

EMA_FAST = 10
EMA_SLOW = 20
```

---

## Running

```bash
python main.py
```

The bot will:

* Check EMA signals
* Open/close trades safely
* Update trailing Stop Loss
* Send notifications **only to the channel**

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

## Live Demo

See alerts in the Telegram channel: [@ajjfklajfklajfkljkl](https://t.me/ajjfklajfklajfkljkl)
