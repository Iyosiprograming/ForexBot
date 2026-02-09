import MetaTrader5 as mt5
from config import *
from telegram import send_telegram
from datetime import date

trades_today = 0
last_trade_day = None

# -------------------------------
# Helpers
# -------------------------------

def calculate_lot():
    acc = mt5.account_info()
    risk_amount = acc.balance * (RISK_PERCENT / 100)
    lot = round(risk_amount / 100, 2)
    return max(lot, 0.01)

def get_position():
    positions = mt5.positions_get(symbol=Trade_Symbol)
    return positions[0] if positions else None

def daily_limit_reached():
    global trades_today, last_trade_day
    today = date.today()
    if last_trade_day != today:
        trades_today = 0
        last_trade_day = today
    return trades_today >= MAX_TRADES_PER_DAY

# -------------------------------
# Open trade
# -------------------------------

def open_trade(signal):
    global trades_today

    if daily_limit_reached():
        print("🚫 Daily limit reached")
        return

    tick = mt5.symbol_info_tick(Trade_Symbol)
    symbol = mt5.symbol_info(Trade_Symbol)

    if symbol.spread > 30:
        print("🚫 Spread too high")
        return

    lot = calculate_lot()
    point = symbol.point

    if signal == "BUY":
        price = tick.ask
        sl = price - STOP_LOSS_PIPS * point
        tp = price + TAKE_PROFIT_PIPS * point
        order_type = mt5.ORDER_TYPE_BUY
    else:
        price = tick.bid
        sl = price + STOP_LOSS_PIPS * point
        tp = price - TAKE_PROFIT_PIPS * point
        order_type = mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Trade_Symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        trades_today += 1
        send_telegram(f"📊 {signal} OPENED | lot: {lot} | SL: {sl:.5f} | TP: {tp:.5f}")
        print(f"{signal} trade executed")
    else:
        print(f"❌ Order failed: {result.retcode}")

# -------------------------------
# Trailing stop
# -------------------------------

def trailing_sl():
    if not USE_TRAILING_SL:
        return

    position = get_position()
    if not position:
        return

    tick = mt5.symbol_info_tick(Trade_Symbol)
    point = mt5.symbol_info(Trade_Symbol).point

    # Calculate profit in pips
    if position.type == mt5.POSITION_TYPE_BUY:
        profit_pips = (tick.bid - position.price_open) / point
        # Move to breakeven
        if profit_pips >= BREAKEVEN_R * STOP_LOSS_PIPS and (position.sl < position.price_open or position.sl == 0):
            modify_sl(position, position.price_open, "BREAKEVEN")
        # Start trailing
        elif profit_pips >= TRAIL_START_R * STOP_LOSS_PIPS:
            new_sl = tick.bid - STOP_LOSS_PIPS * point
            modify_sl(position, new_sl, "TRAILING")
    else:
        profit_pips = (position.price_open - tick.ask) / point
        if profit_pips >= BREAKEVEN_R * STOP_LOSS_PIPS and (position.sl > position.price_open or position.sl == 0):
            modify_sl(position, position.price_open, "BREAKEVEN")
        elif profit_pips >= TRAIL_START_R * STOP_LOSS_PIPS:
            new_sl = tick.ask + STOP_LOSS_PIPS * point
            modify_sl(position, new_sl, "TRAILING")

# -------------------------------
# Modify SL
# -------------------------------

def modify_sl(position, new_sl, phase="TRAILING"):
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": position.ticket,
        "sl": new_sl,
        "tp": position.tp
    }
    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        send_telegram(f"🔧 {phase} - SL moved to {new_sl:.5f}")

# -------------------------------
# Monitor TP/SL
# -------------------------------

def monitor_tp_sl():
    position = get_position()
    if not position:
        return

    tick = mt5.symbol_info_tick(Trade_Symbol)
    if position.type == mt5.POSITION_TYPE_BUY:
        if position.tp > 0 and tick.bid >= position.tp:
            close_position(position, "TP")
        elif position.sl > 0 and tick.bid <= position.sl:
            close_position(position, "SL")
    else:
        if position.tp > 0 and tick.ask <= position.tp:
            close_position(position, "TP")
        elif position.sl > 0 and tick.ask >= position.sl:
            close_position(position, "SL")

def close_position(position, reason="Manual"):
    tick = mt5.symbol_info_tick(Trade_Symbol)
    if position.type == mt5.POSITION_TYPE_BUY:
        price = tick.bid
    else:
        price = tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": position.ticket,
        "type": mt5.ORDER_TYPE_BUY if position.type == mt5.POSITION_TYPE_SELL else mt5.ORDER_TYPE_SELL,
        "volume": position.volume,
        "price": price,
        "deviation": DEVIATION,
        "magic": MAGIC
    }
    mt5.order_send(request)
    send_telegram(f"❌ Position closed | Reason: {reason}")
