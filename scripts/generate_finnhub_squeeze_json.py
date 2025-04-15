import requests
import json

API_KEY = "cvut1tpr01qjg13bb9agcvut1tpr01qjg13bb9b0"
BASE_URL = "https://finnhub.io/api/v1"

# Tickers to evaluate (expand this list anytime)
tickers = ["GME", "AMC", "FFIE", "CVNA", "BBBYQ", "RDBX", "CRKN", "NAKD", "HKD", "TIRX"]

results = []

def fetch_fundamentals(symbol):
    try:
        url = f"{BASE_URL}/stock/metric?symbol={symbol}&metric=all&token={API_KEY}"
        r = requests.get(url)
        data = r.json().get("metric", {})
        return data
    except Exception as e:
        print(f"Error for {symbol}: {e}")
        return {}

for ticker in tickers:
    print(f"Checking {ticker}...")
    data = fetch_fundamentals(ticker)

    try:
        float_shares = float(data.get("shareFloat", 0))
        avg_vol = float(data.get("10DayAverageTradingVolume", 0))
        short_ratio = float(data.get("shortPercentFloat", 0)) * 100

        if float_shares < 50_000_000 and short_ratio > 15 and avg_vol < 1_000_000:
            results.append({
                "ticker": ticker,
                "float": f"{float_shares/1e6:.1f}M",
                "short_percent": f"{short_ratio:.1f}%",
                "avg_volume": f"{avg_vol/1e3:.0f}K",
                "notes": "From Finnhub fundamentals"
            })

    except Exception as err:
        print(f"Skipping {ticker} due to parsing issue: {err}")

# Save output
with open("squeeze-radar.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} tickers to squeeze-radar.json")