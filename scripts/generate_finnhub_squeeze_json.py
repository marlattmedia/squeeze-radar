import requests
import json
import os

API_KEY = os.getenv("FINNHUB_API_KEY") or "REPLACE_WITH_YOUR_API_KEY"

tickers = [
    "GME", "AMC", "FFIE", "CVNA", "BBBYQ", "RDBX", "CRKN", "NAKD", "HKD", "TIRX",
    "HOWL", "GRRR", "PLTR", "MRVL", "ENPH", "LUNR", "WOLF", "ZS", "SMCI", "RR",
    "CHPT", "NVAX", "INTC", "NWTG", "BYND", "PLCE", "RIOT", "AMD"
]

results = []

def meets_criteria(float_m, short_pct, avg_vol):
    try:
        return float_m < 50 and short_pct > 15 and avg_vol < 1_000_000
    except:
        return False

for symbol in tickers:
    try:
        profile = requests.get(f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}").json()
        metrics = requests.get(f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={API_KEY}").json().get("metric", {})

        float_shares = float(metrics.get("shareFloat", 0)) / 1_000_000
        short_pct = float(metrics.get("shortPercentFloat", 0)) * 100
        avg_vol = float(metrics.get("10DayAverageTradingVolume", 0))

        if meets_criteria(float_shares, short_pct, avg_vol):
            results.append({
                "ticker": symbol,
                "company": profile.get("name", "Unknown"),
                "float": f"{float_shares:.1f}M",
                "short_percent": f"{short_pct:.1f}%",
                "avg_volume": f"{avg_vol/1_000:.0f}K",
                "notes": "Matches squeeze criteria"
            })
    except Exception as e:
        print(f"Error processing {symbol}: {e}")

with open("squeeze-radar.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Created squeeze-radar.json with {len(results)} matching tickers.")