import MetaTrader5 as mt5
from config import (
    Trade_Symbol,
    Lot_Size,
    Stop_Loss,
    Take_Profit,
    DEVIATION,
    MAGIC,
    USE_TRAILING_SL,
    TRAIL_START_PIPS,
    TRAIL_DISTANCE_PIPS,
    TRAIL_STEP_PIPS,
)
from telegram import send_telegram
import time

# -------------------------
# HELPERS
# -------------------------

def price_to_pips(price_diff):
    symbol = mt5.symbol_info(Trade_Symbol)
    return round(price_diff / symbol.point, 1)


def get_position():
    positions = mt5.positions_get(symbol=Trade_Symbol)
    return positions[0] if positions else None

# -------------------------
# TRADE FUNCTIONS
# -------------------------

def close_position(position):
    tick = mt5.symbol_info_tick(Trade_Symbol)
    order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
    price = tick.bid if order_type == mt5.ORDER_TYPE_SELL else tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Trade_Symbol,
        "volume": position.volume,
        "type": order_type,
        "position": position.ticket,
        "price": price,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "comment": "Close position",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        send_telegram(
            f"❌ POSITION CLOSED\n"
            f"Symbol: {Trade_Symbol}\n"
            f"Ticket: {position.ticket}\n"
            f"Profit: {position.profit:.2f}"
        )

def open_buy():
    tick = mt5.symbol_info_tick(Trade_Symbol)
    symbol = mt5.symbol_info(Trade_Symbol)
    point = symbol.point

    sl = tick.bid - Stop_Loss * point
    tp = tick.bid + Take_Profit * point

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Trade_Symbol,
        "volume": Lot_Size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "comment": "BOT BUY",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        send_telegram(
            f"📈 BUY OPENED\n"
            f"Symbol: {Trade_Symbol}\n"
            f"Entry: {tick.ask}\n"
            f"SL: {sl}\n"
            f"TP: {tp}\n"
            f"Lot: {Lot_Size}\n"
            f"Ticket: {result.order}"
        )

def open_sell():
    tick = mt5.symbol_info_tick(Trade_Symbol)
    symbol = mt5.symbol_info(Trade_Symbol)
    point = symbol.point

    sl = tick.ask + Stop_Loss * point
    tp = tick.ask - Take_Profit * point

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Trade_Symbol,
        "volume": Lot_Size,
        "type": mt5.ORDER_TYPE_SELL,
        "price": tick.bid,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "comment": "BOT SELL",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        send_telegram(
            f"📉 SELL OPENED\n"
            f"Symbol: {Trade_Symbol}\n"
            f"Entry: {tick.bid}\n"
            f"SL: {sl}\n"
            f"TP: {tp}\n"
            f"Lot: {Lot_Size}\n"
            f"Ticket: {result.order}"
        )

# -------------------------
# SIGNAL HANDLER
# -------------------------

def handle_signal(signal):
    if not signal:
        return

    position = get_position()

    if position is None:
        if signal == "BUY":
            open_buy()
        elif signal == "SELL":
            open_sell()
        return

    if signal == "BUY" and position.type == mt5.POSITION_TYPE_SELL:
        close_position(position)
        open_buy()
    elif signal == "SELL" and position.type == mt5.POSITION_TYPE_BUY:
        close_position(position)
        open_sell()

# -------------------------
# TRAILING STOP LOSS
# -------------------------

def trailing_sl():
    if not USE_TRAILING_SL:
        return

    position = get_position()
    if not position:
        return

    symbol = mt5.symbol_info(Trade_Symbol)
    tick = mt5.symbol_info_tick(Trade_Symbol)
    point = symbol.point

    # BUY POSITION
    if position.type == mt5.POSITION_TYPE_BUY:
        profit_pips = price_to_pips(tick.bid - position.price_open)
        if profit_pips < TRAIL_START_PIPS:
            return
        new_sl = tick.bid - TRAIL_DISTANCE_PIPS * point
        if position.sl == 0 or price_to_pips(new_sl - position.sl) >= TRAIL_STEP_PIPS:
            modify_sl(position, new_sl)

    # SELL POSITION
    elif position.type == mt5.POSITION_TYPE_SELL:
        profit_pips = price_to_pips(position.price_open - tick.ask)
        if profit_pips < TRAIL_START_PIPS:
            return
        new_sl = tick.ask + TRAIL_DISTANCE_PIPS * point
        if position.sl == 0 or price_to_pips(position.sl - new_sl) >= TRAIL_STEP_PIPS:
            modify_sl(position, new_sl)

# -------------------------
# MODIFY SL
# -------------------------

def modify_sl(position, new_sl):
    old_sl = position.sl
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": position.ticket,
        "sl": new_sl,
        "tp": position.tp,
    }
    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        moved_pips = price_to_pips(abs(new_sl - old_sl)) if old_sl != 0 else 0
        send_telegram(
            f"🔧 TRAILING SL UPDATED\n"
            f"Ticket: {position.ticket}\n"
            f"Old SL: {old_sl}\n"
            f"New SL: {new_sl}\n"
            f"Moved: {moved_pips} pips"
        )

