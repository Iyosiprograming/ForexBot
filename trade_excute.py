import MetaTrader5 as mt5
from config import Trade_Symbol, Lot_Size, Stop_Loss, Take_Profit, DEVIATION, MAGIC
from telegram import send_telegram

# =========================
# POSITION HELPERS
# =========================

def get_position():
    positions = mt5.positions_get(symbol=Trade_Symbol)
    if positions:
        return positions[0]
    return None

def close_position(position):
    tick = mt5.symbol_info_tick(Trade_Symbol)
    if position.type == mt5.POSITION_TYPE_BUY:
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Trade_Symbol,
        "volume": position.volume,
        "type": order_type,
        "position": position.ticket,
        "price": price,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "comment": "Close opposite",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    mt5.order_send(request)
    print(f"Closed position {position.type} ticket {position.ticket}")

# =========================
# OPEN ORDERS
# =========================
def open_buy():
    tick = mt5.symbol_info_tick(Trade_Symbol)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Trade_Symbol,
        "volume": Lot_Size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "comment": "BOT BUY",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "sl": tick.bid - Stop_Loss * mt5.symbol_info(Trade_Symbol).point,
        "tp": tick.bid + Take_Profit * mt5.symbol_info(Trade_Symbol).point,
    }
    result = mt5.order_send(request)
    print("BUY result:", result)
    send_telegram(f"📈 BUY executed: {Trade_Symbol} at {request['price']}")


def open_sell():
    tick = mt5.symbol_info_tick(Trade_Symbol)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Trade_Symbol,
        "volume": Lot_Size,
        "type": mt5.ORDER_TYPE_SELL,
        "price": tick.bid,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "comment": "BOT SELL",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "sl": tick.ask + Stop_Loss * mt5.symbol_info(Trade_Symbol).point,
        "tp": tick.ask - Take_Profit * mt5.symbol_info(Trade_Symbol).point,
    }
    result = mt5.order_send(request)
    print("SELL result:", result)
    send_telegram(f"📉 SELL executed: {Trade_Symbol} at {request['price']}")

# =========================
# SIGNAL HANDLER
# =========================
def handle_signal(signal):
    """
    signal: "BUY", "SELL", or None
    """
    position = get_position()

    if position is None:
        if signal == "BUY":
            open_buy()
        elif signal == "SELL":
            open_sell()
        return

    # Reverse if opposite signal
    if signal == "BUY" and position.type == mt5.POSITION_TYPE_SELL:
        close_position(position)
        open_buy()
    elif signal == "SELL" and position.type == mt5.POSITION_TYPE_BUY:
        close_position(position)
        open_sell()

# =========================
# SIMPLE TRAILING SL
# =========================
def trailing_sl(distance_points=50):
    position = get_position()
    if not position:
        return

    tick = mt5.symbol_info_tick(Trade_Symbol)
    point = mt5.symbol_info(Trade_Symbol).point

    if position.type == mt5.POSITION_TYPE_BUY:
        new_sl = tick.bid - distance_points * point
        if position.sl == 0 or new_sl > position.sl:
            modify_sl(position, new_sl)
    elif position.type == mt5.POSITION_TYPE_SELL:
        new_sl = tick.ask + distance_points * point
        if position.sl == 0 or new_sl < position.sl:
            modify_sl(position, new_sl)

def modify_sl(position, sl):
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": position.ticket,
        "sl": sl,
        "tp": position.tp,
    }
    mt5.order_send(request)
    print(f"Updated SL for ticket {position.ticket} to {sl}")
    send_telegram(f"🔧 Updated SL for ticket {position.ticket} to {sl}")
