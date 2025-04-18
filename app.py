import json
import os
from flask import Flask, jsonify, render_template, request
import alpaca_trade_api as tradeapi
from flask_cors import CORS

# Flask setup
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app, resources={r"/*": {"origins": "*"}})

# Alpaca API Credentials
API_KEY = "PK07LNGQ7NZN8MZD8KXD"
API_SECRET = "TOCzWoOkm5g74qSTBPXJSBDYxnEIpUIDTj0tdeWD"
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Watchlist persistence file
WATCHLIST_FILE = "watchlist.json"

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    return ["AAPL", "TSLA", "AMZN", "MSFT"]

def save_watchlist():
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(WATCHLIST, f)

# Load the watchlist from file
WATCHLIST = load_watchlist()

def get_stock_prices():
    """Fetch the latest stock prices for all stocks in the WATCHLIST."""
    stock_data = {}
    for stock in WATCHLIST:
        try:
            trade = api.get_latest_trade(stock)
            price = getattr(trade, "price", None) or trade.get("price")
            if price is None:
                raise ValueError("Missing price")
            print(f"Getting price for {stock}: {price}")
            stock_data[stock] = price
        except Exception as e:
            print(f"Error fetching {stock}: {e}")
            stock_data[stock] = f"Error: {str(e)}"
    return stock_data

@app.route('/')
def index():
    """Serve the frontend HTML page."""
    return render_template("index.html")

@app.route('/stocks', methods=['GET'])
def get_stocks():
    """API endpoint to get stock prices."""
    stock_prices = get_stock_prices()
    return jsonify(stock_prices)

@app.route('/add-stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    print("Add Stock Request:", data)
    symbol = data.get("symbol", "").upper()
    if symbol and symbol not in WATCHLIST:
        WATCHLIST.append(symbol)
        save_watchlist()
    return jsonify({"watchlist": WATCHLIST})

@app.route('/remove-stock', methods=['POST'])
def remove_stock():
    data = request.get_json()
    print("Remove Stock Request:", data)
    symbol = data.get("symbol", "").upper()
    if symbol in WATCHLIST:
        WATCHLIST.remove(symbol)
        save_watchlist()
    return jsonify({"watchlist": WATCHLIST})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
