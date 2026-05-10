import streamlit as st
import plotly.graph_objects as go
from data.stock_data import TOP_BUYS, TOP_SELLS
from data.live_prices import get_prices, price_display, format_last_updated


_SPX = [5820, 5910, 5780, 5650, 5210, 5480, 5631]
_SPX_LABELS = ["Nov '25", "Dec '25", "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26"]


def _badge(signal):
    cls = {
        "Strong Buy":"badge-buy","Buy":"badge-buy","Add more":"badge-buy","Keep DCA":"badge-buy",
        "Reduce":"badge-sell","Sell":"badge-sell","Avoid":"badge-sell",
        "Hold only":"badge-hold","Watch":"badge-watch",
    }.get(signal, "badge-hold")
    return f'<span class="{cls}">{signal}</span>'


def _stock_row(ticker, name, signal, price_str, chg_str, chg_color, live):
    dot = "🟢" if live else "⚪"
    return (
        f'<div class="stock-row-item">'
        f'  <div>'
        f'    <span style="font-weight:600;font-size:0.9rem">{ticker}</span>'
        f'    &nbsp;{_badge(signal)}'
        f'    <div style="font-size:0.75rem;opacity:0.55;margin-top:2px">{name}</div>'
        f'  </div>'
        f'  <div style="text-align:right">'
        f'    <div style="font-weight:600;font-size:0.9rem">{dot} {price_str}</div>'
        f'    <div style="font-size:0.72rem;color:{chg_color}">{chg_str} today</div>'
        f'  </div>'
        f'</div>'
    )


def _card(content_html, accent_color=None):
    """Wrap content in a styled transparent card."""
    accent = accent_color or "rgba(29,158,117,0.6)"
    return (
        f'<div style="background:rgba(128,128,128,0.06);border:1px solid rgba(128,128,128,0.15);'
        f'border-radius:16px;padding:1rem 1.25rem;margin-bottom:0.75rem;'
        f'position:relative;overflow:hidden;'
        f'box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:2px;'
        f'background:{accent};border-radius:16px 16px 0 0;"></div>'
        f'{content_html}'
        f'</div>'
    )


def show():
    st.title("📈 MarketIQ Dashboard")

    # ── fetch live prices ────────────────────────────────────────────────────
    all_tickers = list({s["ticker"] for s in TOP_BUYS + TOP_SELLS} | {"VOO", "MSFT", "BRK.B"})
    prices = get_prices(all_tickers)
    any_live = any(v["live"] for v in prices.values())

    if any_live:
        st.caption(f"🟢 Live prices via Yahoo Finance  ·  {format_last_updated()}  ·  Refreshes every 5 min")
    else:
        st.caption("🟡 Using reference prices — live data will load automatically on deployment")

    st.markdown("---")

    # ── top metrics ──────────────────────────────────────────────────────────
    voo = prices.get("VOO", {})
    voo_price = f"${voo.get('price', 0):,.2f}"
    voo_chg   = f"{voo.get('chg', 0):+.2f}%"
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("VOO", voo_price, voo_chg)
    c2.metric("S&P 500", "~5,600", "via ETF")
    c3.metric("Market Mood", "Cautious Bull", "67 / 100")
    c4.metric("Fear & Greed", "58", "Greed zone")
    c5.metric("Your Signal", "Accumulate", "DCA this month")

    st.markdown("---")

    # ── S&P chart ─────────────────────────────────────────────────────────────
    st.subheader("S&P 500 — 6-month trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=_SPX_LABELS, y=_SPX, mode="lines", fill="tozeroy",
        line=dict(color="#1D9E75", width=2.5),
        fillcolor="rgba(29,158,117,0.07)", name="S&P 500",
    ))
    fig.update_layout(
        height=220, margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(128,128,128,0.12)", tickprefix="$", tickformat=",",
                   color="rgba(128,128,128,0.8)"),
        xaxis=dict(gridcolor="rgba(128,128,128,0.12)", color="rgba(128,128,128,0.8)"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── buy / sell lists ──────────────────────────────────────────────────────
    col_buy, col_sell = st.columns(2)

    with col_buy:
        st.subheader("🟢 Top 10 — Buy signals")
        rows_html = ""
        for s in TOP_BUYS:
            p_str, chg_str, chg_color, live = price_display(s["ticker"], prices)
            rows_html += _stock_row(s["ticker"], s["name"], s["signal"], p_str, chg_str, chg_color, live)
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.04);border:1px solid rgba(128,128,128,0.14);'
            f'border-radius:16px;padding:0.25rem 1rem;position:relative;overflow:hidden;">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;'
            f'background:linear-gradient(90deg,#1D9E75,#378ADD);opacity:0.5;border-radius:16px 16px 0 0;"></div>'
            f'{rows_html}</div>',
            unsafe_allow_html=True,
        )

    with col_sell:
        st.subheader("🔴 Top 10 — Sell / Avoid")
        rows_html = ""
        for s in TOP_SELLS:
            p_str, chg_str, chg_color, live = price_display(s["ticker"], prices)
            rows_html += _stock_row(s["ticker"], s["name"], s["signal"], p_str, chg_str, chg_color, live)
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.04);border:1px solid rgba(128,128,128,0.14);'
            f'border-radius:16px;padding:0.25rem 1rem;position:relative;overflow:hidden;">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;'
            f'background:linear-gradient(90deg,#D85A30,#BA7517);opacity:0.5;border-radius:16px 16px 0 0;"></div>'
            f'{rows_html}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── AI advisor cards ──────────────────────────────────────────────────────
    st.subheader("🤖 AI Advisor — Personalized recommendations")
    recs = [
        ("VOO",   "Vanguard S&P 500 ETF",   "Buy / Add",   "#1D9E75",
         "Continue your monthly DCA into VOO. Geopolitical dips are buying opportunities — "
         "DCA investors who held through similar periods historically saw 18–24% gains over 3–5 years.",
         "3–5 yrs", "50–60% of budget", "High"),
        ("MSFT",  "Microsoft",              "Buy",          "#378ADD",
         "AI infrastructure spending is accelerating. Azure + Copilot revenue beat estimates. "
         "Global enterprise cloud adoption is not slowing.",
         "2–4 yrs", "15–20%", "High"),
        ("BRK.B", "Berkshire Hathaway B",   "Hold / Add",   "#BA7517",
         "Buffett's large cash position is a shield. Best defensive compounder in the market — "
         "especially relevant given current trade war uncertainty.",
         "3+ yrs", "10–15%", "Medium"),
    ]
    for ticker, name, action, accent, reason, horizon, alloc, conviction in recs:
        p_str, chg_str, chg_color, live = price_display(ticker, prices)
        live_tag = "🟢 Live" if live else "⚪ Ref."
        inner = (
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
            f'  <div>'
            f'    <span style="font-weight:700;font-size:1rem">{ticker}</span>'
            f'    <span style="opacity:0.55;font-size:0.8rem;margin-left:8px">{name}</span>'
            f'  </div>'
            f'  <div style="display:flex;align-items:center;gap:10px">'
            f'    <span style="font-size:0.85rem;font-weight:600">{p_str}'
            f'      <span style="color:{chg_color};font-size:0.72rem;margin-left:4px">{chg_str}</span>'
            f'      <span style="opacity:0.4;font-size:0.65rem;margin-left:3px">{live_tag}</span>'
            f'    </span>'
            f'    {_badge(action)}'
            f'  </div>'
            f'</div>'
            f'<div style="font-size:0.85rem;opacity:0.75;line-height:1.55;margin-bottom:10px">{reason}</div>'
            f'<div style="display:flex;gap:20px;font-size:0.72rem;opacity:0.55">'
            f'  <span>Hold: <b style="opacity:1">{horizon}</b></span>'
            f'  <span>Allocation: <b style="opacity:1">{alloc}</b></span>'
            f'  <span>Conviction: <b style="opacity:1">{conviction}</b></span>'
            f'</div>'
        )
        st.markdown(_card(inner, accent), unsafe_allow_html=True)

    col_ref, col_btn = st.columns([3, 1])
    with col_btn:
        if st.button("🔄 Refresh prices", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    # ── sector sentiment ──────────────────────────────────────────────────────
    st.subheader("📊 Sector sentiment")
    sectors = [
        ("Tech",        78, "#1D9E75", "Bullish"),
        ("Healthcare",  65, "#1D9E75", "Bullish"),
        ("Energy",      52, "#888780", "Neutral"),
        ("Financials",  48, "#888780", "Neutral"),
        ("Consumer",    38, "#D85A30", "Bearish"),
        ("Real Estate", 33, "#D85A30", "Bearish"),
    ]
    c1, c2 = st.columns(2)
    for i, (sector, pct, color, label) in enumerate(sectors):
        col = c1 if i % 2 == 0 else c2
        col.markdown(
            f'<div style="margin-bottom:12px">'
            f'  <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:5px">'
            f'    <span style="opacity:0.75">{sector}</span>'
            f'    <span style="color:{color};font-weight:700">{label} {pct}%</span>'
            f'  </div>'
            f'  <div class="sent-track">'
            f'    <div class="sent-fill" style="width:{pct}%;background:{color}"></div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )
