from logic import get_signal
from trade_excute import handle_signal, trailing_sl
from config import Sl_Traling_points
from mt5_connect import connect_mt5, shutdown_mt5
import time

if not connect_mt5():
    exit()

while True:
    signal = get_signal()  # "BUY" / "SELL" / None
    handle_signal(signal)
    trailing_sl(Sl_Traling_points)
    time.sleep(60) 
