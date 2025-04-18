import alpaca_trade_api as tradeapi
import time


API_KEY = "PK07LNGQ7NZN8MZD8KXD"
API_SECRET = "TOCzWoOkm5g74qSTBPXJSBDYxnEIpUIDTj0tdeWD"
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Stocks to track
WATCHLIST = ["AAPL", "TSLA", "AMZN", "MSFT"]
# Price alert thresholds
PRICE_ALERTS = {"AAPL": 175, "TSLA": 200, "AMZN": 3300, "MSFT": 300}


def get_stock_price(symbol):
    """Fetch the latest stock price."""
    barset = api.get_latest_trade(symbol)
    return barset.price


def track_stocks():
    """Continuously monitor stock prices."""
    print("Starting stock tracking...")
    while True:
        for stock in WATCHLIST:
            price = get_stock_price(stock)
            print(f"{stock}: ${price:.2f}")
            
            if stock in PRICE_ALERTS and price >= PRICE_ALERTS[stock]:
                print(f"ALERT: {stock} has reached ${price:.2f} (Threshold: ${PRICE_ALERTS[stock]})")
        
        time.sleep(10)  # Check every 10 seconds


if __name__ == "__main__":
    track_stocks()
