"""
live_prices.py
--------------
Fetches real-time stock prices via yfinance (Yahoo Finance — no API key needed).
Prices are cached for 5 minutes so the app doesn't hammer the API on every rerender.
Falls back to the last known price if a fetch fails.
"""

import time
import streamlit as st

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

# Cache TTL in seconds (5 minutes)
CACHE_TTL = 300

# Fallback prices (used only if yfinance fetch fails entirely)
FALLBACK_PRICES = {
    "VOO":   548.00,
    "VTI":   265.00,
    "QQQ":   480.00,
    "SPY":   560.00,
    "MSFT":  427.00,
    "NVDA":  111.00,
    "GOOGL": 172.00,
    "GOOG":  174.00,
    "AMZN":  203.00,
    "META":  576.00,
    "AAPL":  212.00,
    "AVGO":  185.00,
    "TSLA":  248.00,
    "BRK.B": 468.00,
    "BRK.A": 700000.00,
    "JPM":   245.00,
    "V":     350.00,
    "MA":    530.00,
    "UNH":   290.00,
    "LLY":   841.00,
    "JNJ":   158.00,
    "XOM":   108.00,
    "NEE":   73.00,
    "PG":    175.00,
    "KO":    72.00,
    "HD":    390.00,
    "WMT":   98.00,
    "COST":  940.00,
    "MCD":   310.00,
    "NKE":   62.00,
    "NFLX":  1100.00,
    "DIS":   101.00,
    "PYPL":  68.00,
    "CRM":   300.00,
    "ADBE":  380.00,
    "AMD":   102.00,
    "INTC":  21.00,
    "QCOM":  155.00,
    "AMAT":  155.00,
    "LRCX":  680.00,
    "MU":    92.00,
    "TSM":   175.00,
    "ASML":  680.00,
    "LMT":   468.00,
    "RTX":   130.00,
    "NOC":   490.00,
    "GLD":   310.00,
    "SLV":   32.00,
    "O":     55.00,
    "EQIX":  870.00,
    "AMT":   210.00,
    "GS":    560.00,
    "BAC":   42.00,
    "WFC":   74.00,
    "C":     68.00,
    "AXP":   290.00,
    "PFE":   27.00,
    "MRK":   92.00,
    "ABBV":  195.00,
    "BMY":   58.00,
    "CVX":   155.00,
    "COP":   98.00,
    "SLB":   42.00,
    "UBER":  82.00,
    "ABNB":  125.00,
    "SHOP":  105.00,
    "COIN":  205.00,
    "PLTR":  120.00,
    "SNOW":  155.00,
    "DDOG":  105.00,
    "NET":   115.00,
    "ZS":    195.00,
    "CRWD":  370.00,
    "NOW":   870.00,
    "WDAY":  245.00,
    "MELI":  2100.00,
    "BABA":  87.00,
    "NIO":   3.50,
    "RIVN":  10.00,
    "F":     11.00,
    "GM":    48.00,
    "TM":    185.00,
    "BA":    175.00,
    "CAT":   320.00,
    "DE":    420.00,
    "HON":   225.00,
    "SOFI":  12.00,
    "NU":    14.00,
}

# yfinance uses BRK-B, not BRK.B — map dot to dash for Yahoo
def _to_yf_ticker(ticker: str) -> str:
    return ticker.replace(".", "-")

def _from_yf_ticker(ticker: str) -> str:
    return ticker.replace("-", ".")


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_prices(tickers: tuple) -> dict:
    """
    Fetch latest close price and daily % change for a tuple of tickers.
    Returns dict: { ticker: {"price": float, "chg": float, "live": bool} }
    Cached for CACHE_TTL seconds by Streamlit.
    """
    result = {}

    if not YFINANCE_AVAILABLE:
        for t in tickers:
            result[t] = {"price": FALLBACK_PRICES.get(t, 0.0), "chg": 0.0, "live": False}
        return result

    yf_tickers = [_to_yf_ticker(t) for t in tickers]

    try:
        raw = yf.download(
            yf_tickers,
            period="2d",
            interval="1d",
            progress=False,
            auto_adjust=True,
            threads=True,
        )
        closes = raw["Close"]

        # Handle single-ticker case (returns Series, not DataFrame)
        if len(tickers) == 1:
            closes = closes.to_frame(name=yf_tickers[0])

        for orig, yf_t in zip(tickers, yf_tickers):
            try:
                price = float(closes[yf_t].iloc[-1])
                prev  = float(closes[yf_t].iloc[-2])
                chg   = (price - prev) / prev * 100
                result[orig] = {"price": round(price, 2), "chg": round(chg, 2), "live": True}
            except Exception:
                result[orig] = {
                    "price": FALLBACK_PRICES.get(orig, 0.0),
                    "chg": 0.0,
                    "live": False,
                }

    except Exception:
        for orig in tickers:
            result[orig] = {
                "price": FALLBACK_PRICES.get(orig, 0.0),
                "chg": 0.0,
                "live": False,
            }

    return result


def get_price(ticker: str) -> dict:
    """Convenience wrapper to get price for a single ticker."""
    return fetch_prices((ticker,)).get(ticker, {"price": 0.0, "chg": 0.0, "live": False})


def get_prices(tickers: list) -> dict:
    """Fetch prices for a list of tickers."""
    return fetch_prices(tuple(tickers))


def price_display(ticker: str, prices: dict) -> tuple:
    """
    Returns (price_str, chg_str, chg_color, is_live).
    Pass the full prices dict from get_prices() to avoid repeated fetches.
    """
    info = prices.get(ticker, {"price": 0.0, "chg": 0.0, "live": False})
    price = info["price"]
    chg   = info["chg"]
    live  = info["live"]

    price_str = f"${price:,.2f}" if price > 0 else "N/A"
    chg_str   = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"
    chg_color = "#1D9E75" if chg >= 0 else "#D85A30"

    return price_str, chg_str, chg_color, live


def format_last_updated() -> str:
    return time.strftime("Last updated: %H:%M:%S UTC", time.gmtime())
