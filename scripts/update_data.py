
import requests
from bs4 import BeautifulSoup
import json
import re
from collections import Counter
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# --- Finviz Scraper ---
def get_finviz_data():
    url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=sh_short_o15,sh_float_u50,sh_avgvol_o100&ft=4"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="table-light")
    if not table:
        return []
    rows = table.find_all("tr", class_="table-dark-row-cp")
    radar_data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 10:
            radar_data.append({
                "ticker": cols[1].text.strip(),
                "short_percent": cols[11].text.strip(),
                "float": cols[10].text.strip(),
                "volume": cols[9].text.strip(),
                "catalyst": "Finviz screener"
            })
    return radar_data

# --- Reddit Sentiment Scraper ---
def extract_tickers(text):
    return re.findall(r"\\$[A-Z]{1,5}|\\b[A-Z]{2,5}\\b", text)

def get_reddit_mentions(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/top/?t=day"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("h3")
    tickers = []
    for title in titles:
        tickers.extend(re.findall(r"\\$?\\b[A-Z]{2,5}\\b", title.text.upper()))
    tickers = [t.replace("$", "") for t in tickers]
    top_mentions = Counter(tickers).most_common(10)
    return [{"ticker": t[0], "mentions": t[1], "subreddit": f"r/{subreddit}"} for t in top_mentions]

# --- StockTwits Mock Scraper ---
def get_stocktwits_sentiment():
    # This is a placeholder, real implementation would require scraping or API.
    return [
        {"ticker": "GME", "mentions": 28, "source": "StockTwits"},
        {"ticker": "AMC", "mentions": 15, "source": "StockTwits"}
    ]

# --- Truth Social Mock Scraper ---
def get_truthsocial_posts():
    return [
        {
            "date": str(datetime.now().date()),
            "content": "They're attacking American companies like GME again!",
            "keywords": ["GME", "stocks", "tariffs"]
        }
    ]

# --- Twitter Sentiment Mock Scraper (ApeWisdom) ---
def get_twitter_sentiment():
    return [
        {"ticker": "GME", "mentions": 102, "source": "ApeWisdom"},
        {"ticker": "BBBY", "mentions": 47, "source": "SwaggyStocks"}
    ]

# --- Master Routine ---
def update_data():
    print("Fetching Finviz data...")
    radar = get_finviz_data()

    print("Fetching Reddit sentiment...")
    reddit_data = get_reddit_mentions("shortsqueeze") + get_reddit_mentions("wallstreetbets")

    print("Generating StockTwits sentiment...")
    stocktwits = get_stocktwits_sentiment()

    print("Scraping Truth Social posts...")
    truth = get_truthsocial_posts()

    print("Scraping Twitter sentiment...")
    twitter = get_twitter_sentiment()

    with open("squeeze-radar.json", "w") as f:
        json.dump(radar, f, indent=2)

    with open("reddit-sentiment.json", "w") as f:
        json.dump(reddit_data, f, indent=2)

    with open("stocktwits-sentiment.json", "w") as f:
        json.dump(stocktwits, f, indent=2)

    with open("truthsocial-sentiment.json", "w") as f:
        json.dump(truth, f, indent=2)

    with open("twitter-sentiment.json", "w") as f:
        json.dump(twitter, f, indent=2)

    print("✅ All data updated.")

if __name__ == "__main__":
    update_data()
