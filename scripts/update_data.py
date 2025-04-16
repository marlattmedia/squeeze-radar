import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from collections import Counter

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# --- Part 1: Finviz Scraping ---
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

# --- Part 2: Reddit Sentiment Scraping ---
def extract_tickers(text):
    return re.findall(r"\\$[A-Z]{1,5}|\\b[A-Z]{2,5}\\b", text)

def get_reddit_mentions(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/top/?t=day"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("h3")

    tickers = []
    for title in titles:
        tickers.extend(extract_tickers(title.text.upper()))

    # Clean tickers like $GME → GME
    tickers = [t.replace("$", "") for t in tickers]
    top_mentions = Counter(tickers).most_common(10)

    return [{"ticker": t[0], "mentions": t[1], "subreddit": f"r/{subreddit}"} for t in top_mentions]

# --- Main Update Routine ---
def update_data():
    print("Fetching Finviz data...")
    radar = get_finviz_data()

    print("Fetching Reddit sentiment...")
    reddit_data = get_reddit_mentions("shortsqueeze") + get_reddit_mentions("wallstreetbets")

    with open("squeeze-radar.json", "w") as f:
        json.dump(radar, f, indent=2)

    with open("reddit-sentiment.json", "w") as f:
        json.dump(reddit_data, f, indent=2)

    print("✅ All data updated.")

if __name__ == "__main__":
    update_data()
