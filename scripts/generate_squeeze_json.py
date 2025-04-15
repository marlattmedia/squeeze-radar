import yfinance as yf
import json

# Define a list of high-interest tickers
tickers = ['GME', 'AMC', 'FFIE', 'CVNA', 'BBBYQ', 'RDBX', 'CRKN', 'NAKD', 'HKD', 'TIRX']
results = []

def meets_criteria(info):
    try:
        float_m = info.get('floatShares', 0) / 1e6
        short_pct = info.get('shortPercentOfFloat', 0) * 100
        avg_vol = info.get('averageVolume', 0)
        return float_m < 50 and short_pct > 15 and avg_vol < 1_000_000
    except:
        return False

for symbol in tickers:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        if meets_criteria(info):
            results.append({
                "ticker": symbol,
                "company": info.get("shortName", "N/A"),
                "float": f"{info.get('floatShares', 0) / 1e6:.1f}M",
                "short_percent": f"{info.get('shortPercentOfFloat', 0) * 100:.1f}%",
                "avg_volume": f"{info.get('averageVolume', 0) / 1000:.0f}K",
                "notes": "Auto-generated from yFinance"
            })
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# Save to squeeze-radar.json
with open('squeeze-radar.json', 'w') as f:
    json.dump(results, f, indent=2)
