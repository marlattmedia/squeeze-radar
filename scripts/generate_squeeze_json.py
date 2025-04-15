import requests
from bs4 import BeautifulSoup
import json

FINVIZ_URL = "https://finviz.com/screener.ashx?v=111&f=sh_avgvol_u1000,sh_float_u50,sh_short_o15&o=-shortinterest"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_finviz_stocks():
    response = requests.get(FINVIZ_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table-light")
    
    if not table:
        print("❌ Finviz table not found.")
        return []

    stocks = []
    rows = table.find_all("tr", class_="table-dark-row-cp")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            stocks.append({
                "ticker": cols[1].text.strip(),
                "company": cols[2].text.strip(),
                "float": "Under 50M",
                "short_percent": "Over 15%",
                "avg_volume": "Under 1M",
                "notes": "🧠 Matched Finviz Screener"
            })
    return stocks

def save_to_json(data):
    with open("squeeze-radar.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {len(data)} tickers to squeeze-radar.json")

if __name__ == "__main__":
    stocks = fetch_finviz_stocks()
    save_to_json(stocks)
