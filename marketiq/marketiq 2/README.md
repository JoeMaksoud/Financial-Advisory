# MarketIQ — AI Investment Advisor

A Streamlit dashboard that translates global news and market signals into
personalized stock recommendations, mood-based allocation plans, and
compound-growth projections.

## Features

| Page | What it does |
|---|---|
| **Dashboard** | Live market overview, top-10 buy & sell lists, AI advisor picks, sector sentiment |
| **News → Stocks** | Every global event translated into specific buy / hold / avoid actions |
| **Mood Allocator** | Pick Ambitious / Cautious / Curious, enter an amount, get a budget split |
| **Projection Calculator** | Multi-stock DCA projections with bear / base / bull scenarios |

## Quick start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/marketiq.git
cd marketiq

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Deploy to Streamlit Cloud

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, set **Main file path** to `app.py`.
4. Click **Deploy** — done.

## Project structure

```
marketiq/
├── app.py                  # Entry point + sidebar navigation
├── requirements.txt
├── data/
│   └── stock_data.py       # Stocks, news events, mood profiles
└── pages/
    ├── dashboard.py        # Main dashboard
    ├── news_stocks.py      # News → stock recommendations
    ├── mood_allocator.py   # Mood-based budget split
    └── projection.py       # DCA projection calculator
```

## Connecting live data (optional)

Replace the static dicts in `data/stock_data.py` with API calls:

| Data | Suggested API |
|---|---|
| Real-time prices | [Yahoo Finance (yfinance)](https://pypi.org/project/yfinance/) |
| News headlines | [NewsAPI](https://newsapi.org) or [Finnhub](https://finnhub.io) |
| Sentiment scores | [Finnhub sentiment](https://finnhub.io/docs/api/news-sentiment) |

## Disclaimer

This app is for educational and informational purposes only.
It is **not financial advice**. Always consult a licensed financial advisor
before making investment decisions.
