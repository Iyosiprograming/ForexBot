from logic import get_signal
from trade_excute import handle_signal, trailing_sl
from config import USE_TRAILING_SL
from mt5_connect import connect_mt5, shutdown_mt5
import time

# Connect to MT5
if not connect_mt5():
    exit()

# Main loop
try:
    while True:
        signal = get_signal()  # "BUY" / "SELL" / None
        handle_signal(signal)
        if USE_TRAILING_SL:
            trailing_sl()      
        time.sleep(1)
finally:
    shutdown_mt5()
