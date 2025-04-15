name: 🧠 Update Squeeze Radar from Finnhub

on:
  workflow_dispatch:
  schedule:
    - cron: '0 11 * * 1-5'  # 7 AM ET, Mon–Fri

jobs:
  update-radar:
    runs-on: ubuntu-latest

    steps:
      - name: 🛒 Checkout Repo
        uses: actions/checkout@v3

      - name: 🐍 Set Up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: 📦 Install Dependencies
        run: pip install requests

      - name: 🧠 Generate squeeze-radar.json (Finnhub)
        run: python scripts/generate_finnhub_squeeze_json.py

      - name: 💾 Commit and Push JSON
        run: |
          git config user.name "marlattmedia"
          git config user.email "actions@github.com"
          git add squeeze-radar.json
          git commit -m "📊 Auto-update squeeze radar (Finnhub)"
          git push
