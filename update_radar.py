import json
from datetime import datetime

# This function will eventually scrape Finviz, Reddit, Yahoo, etc.
# For now it simulates the output
def fetch_squeeze_candidates():
    # Simulated data – replace with scraped data
    return [
        {
            "ticker": "GME",
            "company": "GameStop Corp.",
            "float": "45M",
            "short_percent": "22.1%",
            "avg_volume": "950K",
            "notes": "🔥 High retail interest on Reddit"
        },
        {
            "ticker": "CRKN",
            "company": "Crown ElectroKinetics",
            "float": "8M",
            "short_percent": "28.9%",
            "avg_volume": "620K",
            "notes": "🧲 Low float, chatter on Stocktwits"
        }
    ]

def main():
    print("Fetching squeeze candidates...")
    candidates = fetch_squeeze_candidates()
    
    with open("squeeze-radar.json", "w") as f:
        json.dump(candidates, f, indent=2)
    
    print(f"Updated squeeze-radar.json with {len(candidates)} tickers.")

if __name__ == "__main__":
    main()
