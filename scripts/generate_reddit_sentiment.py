import requests
import json

subreddits = ["wallstreetbets", "shortsqueeze", "stocks"]
reddit_data = []
headers = {"User-Agent": "Mozilla/5.0"}

rank = 1
for subreddit in subreddits:
    try:
        url = f"https://yolostocks.live/r/{subreddit}/hourly"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        mentions = response.json()

        for item in mentions[:3]:  # top 3 per subreddit
            reddit_data.append({
                "subreddit": subreddit,
                "ticker": item["ticker"],
                "mentions": item["mentions"],
                "rank": rank
            })
            rank += 1
    except Exception as e:
        print(f"Failed to pull {subreddit}: {e}")

# Save to JSON
with open("reddit-sentiment.json", "w") as f:
    json.dump(reddit_data, f, indent=2)
