import json
from datetime import datetime

# Simulated data (replace this with scraping/API logic)
squeeze_radar = [
    {"ticker": "GME", "short_percent": "22%", "float": "30M", "volume": "500,000", "catalyst": "Reddit buzz"},
    {"ticker": "FFAI", "short_percent": "18%", "float": "12M", "volume": "850,000", "catalyst": "Low float runner"},
]

reddit_sentiment = [
    {"ticker": "GME", "mentions": 1420, "subreddit": "r/wallstreetbets"},
    {"ticker": "FFAI", "mentions": 545, "subreddit": "r/shortsqueeze"},
]

# Write to JSON files
with open("squeeze-radar.json", "w") as f:
    json.dump(squeeze_radar, f, indent=2)

with open("reddit-sentiment.json", "w") as f:
    json.dump(reddit_sentiment, f, indent=2)

print(f"[{datetime.now()}] Data updated successfully.")
