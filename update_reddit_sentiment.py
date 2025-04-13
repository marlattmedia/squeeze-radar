# Triggering manual test

import json
import requests

sources = {
    "r/stocks": "https://yolostocks.live/r/stocks/hourly",
    "r/wallstreetbets": "https://yolostocks.live/r/wallstreetbets/hourly",
    "r/shortsqueeze": "https://yolostocks.live/r/shortsqueeze/hourly"
}

combined_data = []

for subreddit, url in sources.items():
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        for i, entry in enumerate(data):
            combined_data.append({
                "subreddit": subreddit,
                "ticker": entry.get("ticker", "").upper(),
                "mentions": entry.get("mentions", 0),
                "rank": i + 1
            })
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

with open("reddit-sentiment.json", "w") as f:
    json.dump(combined_data, f, indent=2)
