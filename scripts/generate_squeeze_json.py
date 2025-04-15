
import json
from datetime import datetime

# Simulated stock data (replace with real scraping or API pull later)
candidates = [
    {"ticker": "GME", "company": "GameStop Corp.", "float": 45, "short_percent": 22.1, "volume": 950000, "avg_volume": 1200000, "notes": "🔥 Retail interest"},
    {"ticker": "FFAI", "company": "Future Fintech", "float": 6.2, "short_percent": 18.7, "volume": 540000, "avg_volume": 900000, "notes": "✅ Low float"},
    {"ticker": "XYZC", "company": "Zebra Chip Co", "float": 62.1, "short_percent": 12.5, "volume": 450000, "avg_volume": 1100000, "notes": "❌ Float too high"},
    {"ticker": "CRKN", "company": "Crown ElectroKinetics", "float": 4.8, "short_percent": 29.8, "volume": 820000, "avg_volume": 1000000, "notes": "⚡ Reddit momentum"},
    {"ticker": "NAKD", "company": "Cenntro Electric", "float": 7.1, "short_percent": 11.3, "volume": 410000, "avg_volume": 750000, "notes": "Too low short %"}
]

# Filter based on screener logic
filtered = []
for stock in candidates:
    if stock["float"] < 50 and stock["short_percent"] > 15 and stock["volume"] < 1000000:
        filtered.append({
            "ticker": stock["ticker"],
            "company": stock["company"],
            "float": f"{stock['float']}M",
            "short_percent": f"{stock['short_percent']}%",
            "current_volume": f"{int(stock['volume']/1000)}K",
            "avg_volume": f"{int(stock['avg_volume']/1000)}K",
            "notes": stock["notes"]
        })

# Write to JSON
with open("squeeze-radar.json", "w") as f:
    json.dump(filtered, f, indent=2)

print(f"✅ squeeze-radar.json updated at {datetime.utcnow()} UTC")
