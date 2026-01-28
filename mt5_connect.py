import MetaTrader5 as mt5

def connect_mt5():
    if not mt5.initialize():
        print("MT5 init failed:", mt5.last_error())
        return False

    account = mt5.account_info()
    if account is None:
        print("Failed to get account info")
        return False

    print(f"Connected to MT5 | Account: {account.login}")
    return True


if __name__ == "__main__":
    if connect_mt5():
        mt5.shutdown()
