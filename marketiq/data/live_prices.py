"""
live_prices.py — Live prices via yfinance. NEVER shows N/A.
If market is closed or fetch fails, shows last known price with a clear label.
"""
import time
import streamlit as st

try:
    import yfinance as yf
    YFINANCE_OK = True
except ImportError:
    YFINANCE_OK = False

CACHE_TTL = 300  # 5 minutes

# ── Last-known prices (May 2026) — shown when market closed or fetch fails ────
LAST_KNOWN = {
    "VOO": 678.10, "VTI": 252.40, "QQQ": 490.20, "QQQM": 198.40,
    "SPY": 601.80, "SOXX": 212.30, "ITA": 148.60, "SCHD": 28.40,
    "VGK": 74.20, "EWJ": 72.10, "VWO": 44.80, "VNQ": 82.30,
    "ARKK": 48.20, "TLT": 88.20, "XLE": 88.40, "GLD": 310.20,
    "NVDA": 215.16, "AAPL": 293.41, "MSFT": 415.17, "AMZN": 272.66,
    "GOOGL": 170.50, "GOOG": 172.00, "META": 609.53, "TSLA": 427.99,
    "AVGO": 429.17, "AMD": 102.40, "INTC": 21.30, "QCOM": 155.80,
    "AMAT": 155.40, "ASML": 680.00, "SAP": 242.80, "APP": 312.40,
    "MELI": 2100.00, "SE": 112.40, "CELH": 31.20,
    "BRK.B": 468.00, "JPM": 245.30, "GS": 560.20, "BAC": 42.10,
    "LLY": 841.00, "ABBV": 195.20, "MRK": 92.10, "PFE": 27.30,
    "XOM": 108.20, "CVX": 155.10, "LMT": 468.10, "RTX": 130.20,
    "NEE": 73.20, "O": 55.10, "EQIX": 870.20, "DIS": 101.30,
    "NFLX": 1100.00, "NIO": 3.50, "BABA": 87.10,
    "DIA": 488.20, "XLF": 44.20, "XLV": 148.30, "IBB": 148.50,
    "XAR": 142.10, "XLY": 212.30,
}


def _yf_ticker(t: str) -> str:
    return t.replace(".", "-")


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_prices(tickers: tuple) -> dict:
    """
    Returns dict: { ticker: {"price": float, "chg": float, "status": str} }
    status: "live" | "closed" | "fallback"
    NEVER returns None or N/A — always shows last known price.
    """
    result = {}

    if not YFINANCE_OK:
        for t in tickers:
            result[t] = {"price": LAST_KNOWN.get(t, 0.0), "chg": 0.0, "status": "fallback"}
        return result

    yf_map = {t: _yf_ticker(t) for t in tickers}
    yf_list = list(yf_map.values())

    try:
        raw = yf.download(
            yf_list, period="5d", interval="1d",
            progress=False, auto_adjust=True, threads=True,
        )
        closes = raw["Close"] if "Close" in raw else raw

        # Handle single-ticker case
        if len(tickers) == 1:
            closes = closes.to_frame(name=yf_list[0])

        # Drop rows where ALL values are NaN (non-trading days)
        closes = closes.dropna(how="all")

        for orig, yf_t in yf_map.items():
            try:
                col = closes[yf_t].dropna()
                if len(col) == 0:
                    raise ValueError("empty")
                price = float(col.iloc[-1])
                prev  = float(col.iloc[-2]) if len(col) >= 2 else price
                chg   = (price - prev) / prev * 100 if prev else 0.0

                # If price is suspiciously 0 or NaN use fallback
                if price <= 0 or price != price:
                    raise ValueError("bad price")

                # Determine if market is open (last data within 24h of now)
                last_ts = col.index[-1]
                try:
                    age_hours = (time.time() - last_ts.timestamp()) / 3600
                    status = "live" if age_hours < 18 else "closed"
                except Exception:
                    status = "closed"

                result[orig] = {"price": round(price, 2), "chg": round(chg, 2), "status": status}

            except Exception:
                result[orig] = {
                    "price": LAST_KNOWN.get(orig, 0.0),
                    "chg": 0.0,
                    "status": "fallback",
                }

    except Exception:
        for orig in tickers:
            result[orig] = {
                "price": LAST_KNOWN.get(orig, 0.0),
                "chg": 0.0,
                "status": "fallback",
            }

    return result


def get_prices(tickers: list) -> dict:
    return fetch_prices(tuple(sorted(set(tickers))))


def price_display(ticker: str, prices: dict) -> tuple:
    """Returns (price_str, chg_str, chg_color, status_label, status_icon)"""
    info   = prices.get(ticker, {"price": LAST_KNOWN.get(ticker, 0.0), "chg": 0.0, "status": "fallback"})
    price  = info["price"]
    chg    = info["chg"]
    status = info.get("status", "fallback")

    price_str = f"${price:,.2f}" if price > 0 else f"${LAST_KNOWN.get(ticker, 0):,.2f}"
    chg_str   = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"
    chg_color = "#1D9E75" if chg >= 0 else "#D85A30"

    status_icons = {"live": "🟢", "closed": "🕐", "fallback": "⚪"}
    status_labels = {"live": "Live", "closed": "Last close", "fallback": "Ref."}

    return price_str, chg_str, chg_color, status_labels[status], status_icons[status]


def format_last_updated() -> str:
    return time.strftime("Last updated: %H:%M:%S UTC", time.gmtime())
