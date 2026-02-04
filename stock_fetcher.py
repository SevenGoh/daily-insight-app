import yfinance as yf
import pandas as pd

# Stock Tickers Configuration
TICKERS = {
    "world": [
        "^GSPC", "^IXIC", "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "BRK-B"
    ],
    "malaysia": [
        "^KLSE", "1155.KL", "1023.KL", "1295.KL", "5183.KL", "5225.KL", "6033.KL", "5347.KL", "4065.KL", "5819.KL"
    ]
}

def get_stock_data(tickers):
    """
    Fetches current price and daily change for a list of tickers.
    """
    data = []
    
    # Download data for all tickers at once (efficient)
    tickers_str = " ".join(tickers)
    try:
        # period="5d" to ensure we get enough history for calculation if market is closed
        df = yf.download(tickers_str, period="5d", progress=False)
        
        # Calculate daily change
        # Access 'Close' prices
        close_prices = df["Close"]
        
        for ticker in tickers:
            try:
                # Get the last two available closing prices
                series = close_prices[ticker].dropna()
                if len(series) < 2:
                    continue
                
                last_price = series.iloc[-1]
                prev_price = series.iloc[-2]
                change = last_price - prev_price
                pct_change = (change / prev_price) * 100
                
                data.append({
                    "ticker": ticker,
                    "price": last_price,
                    "change": change,
                    "pct_change": pct_change,
                    "abs_change": abs(pct_change) # for sorting by impact
                })
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                
    except Exception as e:
        print(f"Error downloading stock data: {e}")
        return []

    return data

def fetch_top_stocks(category="world", limit=5):
    """
    Fetches stock data and returns the top `limit` stocks sorted by absolute percentage change (volatility).
    """
    if category not in TICKERS:
        return []

    print(f"Fetching {category} stocks...")
    stock_data = get_stock_data(TICKERS[category])
    
    # Sort by absolute percentage change (descending) to find biggest movers
    sorted_stocks = sorted(stock_data, key=lambda x: x["abs_change"], reverse=True)
    
    return sorted_stocks[:limit]

if __name__ == "__main__":
    # Test run
    print("--- TOP 5 WORLD STOCKS ---")
    world_stocks = fetch_top_stocks("world", 5)
    for s in world_stocks:
        print(f"{s['ticker']}: {s['price']:.2f} ({s['pct_change']:.2f}%)")
    
    print("\n--- TOP 5 MALAYSIA STOCKS ---")
    my_stocks = fetch_top_stocks("malaysia", 5)
    for s in my_stocks:
        print(f"{s['ticker']}: {s['price']:.2f} ({s['pct_change']:.2f}%)")
