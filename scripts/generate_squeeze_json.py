
import requests
from bs4 import BeautifulSoup
import json

FINVIZ_URL = "https://finviz.com/screener.ashx?v=111&f=sh_avgvol_o500,sh_float_u50,sh_price_o1,sh_short_o15&ft=4&o=-short"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_finviz_tickers():
    response = requests.get(FINVIZ_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table-light")
    
    tickers = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 2:
            ticker = cols[1].text.strip()
            tickers.append(ticker)
    return tickers

def fetch_yahoo_data(ticker):
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics,summaryDetail"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return None

    try:
        data = r.json()["quoteSummary"]["result"][0]
        stats = data["defaultKeyStatistics"]
        summary = data["summaryDetail"]
        float_shares = stats.get("sharesOutstanding", {}).get("raw", 0)
        short_percent = stats.get("shortPercentOfFloat", {}).get("raw", 0)
        avg_vol = summary.get("averageVolume", {}).get("raw", 0)
        cur_vol = summary.get("volume", {}).get("raw", 0)

        return {
            "float": round(float_shares / 1_000_000, 1),
            "short_percent": round(short_percent * 100, 1),
            "avg_volume": int(avg_vol),
            "volume": int(cur_vol)
        }
    except Exception:
        return None

def generate_json():
    tickers = fetch_finviz_tickers()
    result = []

    for ticker in tickers:
        info = fetch_yahoo_data(ticker)
        if not info:
            continue

        if info["float"] < 50 and info["short_percent"] > 15 and info["volume"] < 1_000_000:
            result.append({
                "ticker": ticker,
                "company": "",
                "float": f"{info['float']}M",
                "short_percent": f"{info['short_percent']}%",
                "avg_volume": f"{int(info['avg_volume'] / 1000)}K",
                "current_volume": f"{int(info['volume'] / 1000)}K",
                "notes": "✅ Matches squeeze criteria"
            })

    with open("squeeze-radar.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    generate_json()
