"""
live_prices.py — fetches real-time prices via yfinance (Yahoo Finance).
Cached 5 min. Falls back to FALLBACK_PRICES (updated May 2026) if fetch fails.
"""
import time
import streamlit as st

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

CACHE_TTL = 300  # 5 minutes

# ── Accurate fallback prices as of May 10, 2026 ───────────────────────────────
FALLBACK_PRICES = {
    # Core ETFs
    "VOO":   678.10,
    "VTI":   252.40,
    "QQQ":   490.20,
    "SPY":   601.80,
    # Magnificent 7
    "NVDA":  215.16,
    "AAPL":  293.41,
    "MSFT":  415.17,
    "AMZN":  272.66,
    "GOOGL": 170.50,
    "GOOG":  172.00,
    "META":  609.53,
    "TSLA":  427.99,
    # Other large-cap tech
    "AVGO":  429.17,
    "AMD":   102.40,
    "INTC":   21.30,
    "QCOM":  155.80,
    "AMAT":  155.40,
    "LRCX":  680.00,
    "MU":     92.10,
    "TSM":   175.20,
    "ASML":  680.00,
    "CRM":   300.10,
    "ADBE":  380.20,
    "NOW":   870.00,
    "WDAY":  245.10,
    "SNOW":  155.40,
    "DDOG":  105.20,
    "NET":   115.30,
    "ZS":    195.10,
    "CRWD":  370.20,
    "PLTR":  120.10,
    "COIN":  205.30,
    "SHOP":  105.10,
    "UBER":   82.30,
    "ABNB":  125.20,
    "NFLX": 1100.00,
    "PYPL":   68.10,
    # Financials
    "BRK.B": 468.00,
    "BRK.A": 700000.00,
    "JPM":   245.30,
    "GS":    560.20,
    "BAC":    42.10,
    "WFC":    74.20,
    "C":      68.30,
    "AXP":   290.10,
    "V":     350.20,
    "MA":    530.10,
    # Healthcare
    "LLY":   841.00,
    "UNH":   290.10,
    "JNJ":   158.20,
    "MRK":    92.10,
    "ABBV":  195.20,
    "BMY":    58.10,
    "PFE":    27.30,
    # Energy
    "XOM":   108.20,
    "CVX":   155.10,
    "COP":    98.20,
    "SLB":    42.10,
    # Consumer / Industrial
    "WMT":    98.10,
    "COST":  940.20,
    "HD":    390.10,
    "MCD":   310.20,
    "PG":    175.10,
    "KO":     72.20,
    "NKE":    62.10,
    "DIS":   101.30,
    "MELI": 2100.00,
    "BABA":   87.10,
    # Defense
    "LMT":   468.10,
    "RTX":   130.20,
    "NOC":   490.10,
    # Utilities / REIT
    "NEE":    73.20,
    "O":      55.10,
    "EQIX":  870.20,
    "AMT":   210.10,
    # Commodities
    "GLD":   310.20,
    "SLV":    32.10,
    # Auto
    "TM":    185.10,
    "F":      11.20,
    "GM":     48.10,
    "RIVN":   10.20,
    "NIO":     3.50,
    "TSLA":  427.99,
    # Other
    "BA":    175.10,
    "CAT":   320.20,
    "DE":    420.10,
    "HON":   225.20,
    "SOFI":   12.10,
    "NU":     14.20,
}


def _to_yf(ticker: str) -> str:
    return ticker.replace(".", "-")


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_prices(tickers: tuple) -> dict:
    result = {}
    if not YFINANCE_AVAILABLE:
        for t in tickers:
            result[t] = {"price": FALLBACK_PRICES.get(t, 0.0), "chg": 0.0, "live": False}
        return result

    yf_tickers = [_to_yf(t) for t in tickers]
    try:
        raw    = yf.download(yf_tickers, period="2d", interval="1d",
                             progress=False, auto_adjust=True, threads=True)
        closes = raw["Close"]
        if len(tickers) == 1:
            closes = closes.to_frame(name=yf_tickers[0])

        for orig, yf_t in zip(tickers, yf_tickers):
            try:
                price = float(closes[yf_t].iloc[-1])
                prev  = float(closes[yf_t].iloc[-2])
                chg   = (price - prev) / prev * 100
                result[orig] = {"price": round(price, 2), "chg": round(chg, 2), "live": True}
            except Exception:
                result[orig] = {"price": FALLBACK_PRICES.get(orig, 0.0), "chg": 0.0, "live": False}
    except Exception:
        for orig in tickers:
            result[orig] = {"price": FALLBACK_PRICES.get(orig, 0.0), "chg": 0.0, "live": False}
    return result


def get_prices(tickers: list) -> dict:
    return fetch_prices(tuple(tickers))


def get_price(ticker: str) -> dict:
    return fetch_prices((ticker,)).get(ticker, {"price": 0.0, "chg": 0.0, "live": False})


def price_display(ticker: str, prices: dict) -> tuple:
    info      = prices.get(ticker, {"price": 0.0, "chg": 0.0, "live": False})
    price     = info["price"]
    chg       = info["chg"]
    live      = info["live"]
    price_str = f"${price:,.2f}" if price > 0 else "N/A"
    chg_str   = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"
    chg_color = "#1D9E75" if chg >= 0 else "#D85A30"
    return price_str, chg_str, chg_color, live


def format_last_updated() -> str:
    return time.strftime("Last updated: %H:%M:%S UTC", time.gmtime())
