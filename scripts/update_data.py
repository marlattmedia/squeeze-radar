<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>📈 Stock Squeeze Radar Dashboard</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #121212;
      color: #fff;
      margin: 0;
      padding: 0 10px;
    }
    h1, h2, h3 {
      color: #ffcc00;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0;
    }
    th, td {
      border: 1px solid #444;
      padding: 8px;
      text-align: left;
    }
    th {
      background-color: #333;
    }
    tr:nth-child(even) {
      background-color: #1e1e1e;
    }
    button {
      margin-right: 10px;
      padding: 8px 12px;
      border: none;
      background: #333;
      color: #fff;
      cursor: pointer;
      border-radius: 5px;
    }
    .section {
      margin-bottom: 30px;
    }
    .tradingview-widget-container {
      height: 800px;
    }
  </style>
</head>
<body>
  <h1>📈 Squeeze Radar Dashboard</h1>

  <div class="section">
    <h2>📡 Live News & Alerts</h2>
    <ul id="live-news"></ul>
  </div>

  <div class="section">
    <h2>📊 Filter by Avg Volume</h2>
    <button onclick="filterVolume(5000000)">Under 5M</button>
    <button onclick="filterVolume(2000000)">Under 2M</button>
  </div>

  <div class="section">
    <h2>🔥 Short Squeeze Radar</h2>
    <table id="radar-table">
      <thead>
        <tr><th>Ticker</th><th>Short %</th><th>Float</th><th>Volume</th><th>Catalyst</th></tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>

  <div class="section">
    <h2>🧠 Reddit Sentiment Radar</h2>
    <table id="reddit-table">
      <thead>
        <tr><th>Ticker</th><th>Mentions</th><th>Subreddit</th></tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>

  <div class="section">
    <h2>📢 Social Media Trackers</h2>
    <h3>Trump Truth Social (Filtered)</h3>
    <ul id="truth-social-feed"></ul>

    <h3>StockTwits Mentions</h3>
    <ul id="stocktwits-feed"></ul>

    <h3>X (formerly Twitter) Activity</h3>
    <ul id="x-feed"></ul>
  </div>

  <div class="section">
    <h2>📈 TradingView Chart</h2>
    <div class="tradingview-widget-container">
      <div id="tradingview-widget" style="height: 100%;"></div>
    </div>
  </div>

  <script>
    async function loadRadarData() {
      const response = await fetch('https://raw.githubusercontent.com/marlattmedia/squeeze-radar/refs/heads/main/squeeze-radar.json');
      const data = await response.json();
      const tbody = document.querySelector('#radar-table tbody');
      tbody.innerHTML = '';
      data.forEach(stock => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${stock.ticker}</td>
          <td>${stock.short_percent}</td>
          <td>${stock.float}</td>
          <td>${stock.volume}</td>
          <td>${stock.catalyst || ''}</td>
        `;
        tbody.appendChild(row);
      });
    }

    async function loadRedditData() {
      const response = await fetch('https://raw.githubusercontent.com/marlattmedia/squeeze-radar/refs/heads/main/reddit-sentiment.json');
      const data = await response.json();
      const tbody = document.querySelector('#reddit-table tbody');
      tbody.innerHTML = '';
      data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${item.ticker}</td>
          <td>${item.mentions}</td>
          <td>${item.subreddit}</td>
        `;
        tbody.appendChild(row);
      });
    }

    function filterVolume(maxVolume) {
      const rows = document.querySelectorAll('#radar-table tbody tr');
      rows.forEach(row => {
        const volume = parseInt(row.children[3].textContent.replace(/,/g, ''));
        row.style.display = volume <= maxVolume ? '' : 'none';
      });
    }

    window.onload = () => {
      loadRadarData();
      loadRedditData();
    };
  </script>

  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
    new TradingView.widget({
      container_id: "tradingview-widget",
      autosize: true,
      symbol: "NYSE:GME",
      interval: "15",
      timezone: "Etc/UTC",
      theme: "dark",
      style: "1",
      locale: "en",
      toolbar_bg: "#f1f3f6",
      enable_publishing: false,
      allow_symbol_change: true,
      details: true
    });
  </script>
</body>
</html>
