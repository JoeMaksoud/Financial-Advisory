import streamlit as st
import plotly.graph_objects as go
from data.stock_data import TOP_BUYS, TOP_SELLS
from data.live_prices import get_prices, price_display, format_last_updated

# ── Market index historical data (S&P 500 proxy via SPY close prices) ─────────
# Approximate weekly SPY closes for different time windows
CHART_DATA = {
    "1W": {
        "labels": ["Mon May 4","Tue May 5","Wed May 6","Thu May 7","Fri May 8"],
        "spy":    [658.2, 662.5, 672.8, 670.1, 676.4],
        "qqq":    [472.1, 477.3, 486.9, 484.2, 490.8],
        "dia":    [480.3, 482.1, 487.6, 485.9, 488.2],
    },
    "1M": {
        "labels": ["Apr 7","Apr 14","Apr 21","Apr 28","May 5","May 8"],
        "spy":    [601.4, 628.3, 643.7, 657.2, 668.9, 676.4],
        "qqq":    [428.6, 450.2, 461.8, 472.5, 482.1, 490.8],
        "dia":    [456.2, 468.4, 475.6, 480.1, 485.3, 488.2],
    },
    "6M": {
        "labels": ["Nov '25","Dec '25","Jan '26","Feb '26","Mar '26","Apr '26","May '26"],
        "spy":    [582.0, 591.0, 578.0, 565.0, 521.0, 618.0, 676.4],
        "qqq":    [502.3, 512.1, 498.4, 483.2, 441.7, 468.3, 490.8],
        "dia":    [444.2, 452.1, 445.8, 438.3, 421.6, 471.4, 488.2],
    },
    "1Y": {
        "labels": ["May '25","Jul '25","Sep '25","Nov '25","Jan '26","Mar '26","May '26"],
        "spy":    [532.0, 555.0, 543.0, 582.0, 578.0, 521.0, 676.4],
        "qqq":    [444.2, 468.1, 457.3, 502.3, 498.4, 441.7, 490.8],
        "dia":    [398.1, 416.3, 408.7, 444.2, 445.8, 421.6, 488.2],
    },
    "All": {
        "labels": ["2020","2021","2022","2023","2024","2025","2026"],
        "spy":    [321.0, 412.0, 380.0, 452.0, 537.0, 582.0, 676.4],
        "qqq":    [256.3, 382.1, 278.4, 351.2, 449.8, 502.3, 490.8],
        "dia":    [297.4, 352.1, 327.8, 379.5, 421.3, 444.2, 488.2],
    },
}

INDEX_COLORS = {
    "spy": ("#1D9E75", "S&P 500 (SPY)"),
    "qqq": ("#378ADD", "Nasdaq-100 (QQQ)"),
    "dia": ("#BA7517", "Dow Jones (DIA)"),
}


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
        f'<div><span style="font-weight:600;font-size:0.9rem">{ticker}</span>&nbsp;{_badge(signal)}'
        f'<div style="font-size:0.75rem;opacity:0.5;margin-top:2px">{name}</div></div>'
        f'<div style="text-align:right">'
        f'<div style="font-weight:600;font-size:0.9rem">{dot} {price_str}</div>'
        f'<div style="font-size:0.72rem;color:{chg_color}">{chg_str} today</div>'
        f'</div></div>'
    )


def _card(content, accent="rgba(29,158,117,0.6)"):
    return (
        f'<div style="background:rgba(128,128,128,0.06);border:1px solid rgba(128,128,128,0.15);'
        f'border-radius:16px;padding:1rem 1.25rem;margin-bottom:0.75rem;position:relative;overflow:hidden;">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:2px;background:{accent};'
        f'border-radius:16px 16px 0 0;opacity:0.7;"></div>'
        f'{content}</div>'
    )


def show():
    st.markdown('<h2 style="font-size:1.5rem;font-weight:600;margin-bottom:6px;letter-spacing:-0.3px">Market Overview</h2>', unsafe_allow_html=True)

    # ── live prices for key indices via ETF proxies ───────────────────────────
    key_tickers = list({s["ticker"] for s in TOP_BUYS + TOP_SELLS}
                       | {"SPY","QQQ","DIA","^VIX"})
    prices = get_prices(key_tickers)
    any_live = any(v["live"] for v in prices.values())

    col_status, col_refresh = st.columns([4,1])
    with col_status:
        if any_live:
            st.caption(f"🟢 Live data via Yahoo Finance  ·  {format_last_updated()}  ·  Auto-refreshes every 5 min")
        else:
            st.caption("🟡 Reference prices — live data loads automatically on deployment")
    with col_refresh:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    # ── top market metrics panel ──────────────────────────────────────────────
    spy_p, spy_chg, spy_col, _ = price_display("SPY", prices)
    qqq_p, qqq_chg, qqq_col, _ = price_display("QQQ", prices)
    dia_p, dia_chg, dia_col, _ = price_display("DIA", prices)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("S&P 500 (SPY)",    spy_p, spy_chg)
    c2.metric("Nasdaq-100 (QQQ)", qqq_p, qqq_chg)
    c3.metric("Dow Jones (DIA)",  dia_p, dia_chg)
    c4.metric("Market Trend",  "↑ Bullish",  "6th winning week")
    c5.metric("Fear & Greed",  "68 — Greed", "↑ from 58 last wk")
    c6.metric("VIX Volatility","~16",        "Low — calm market")

    # ── key market context strip ──────────────────────────────────────────────
    st.markdown(
        '<div style="background:rgba(29,158,117,0.07);border:1px solid rgba(29,158,117,0.2);'
        'border-radius:12px;padding:10px 16px;margin:12px 0;font-size:0.82rem;opacity:0.85;">'
        '📰 <b>Market pulse (May 10, 2026):</b> S&amp;P 500 at record 7,399 · '
        'Nasdaq +4.5% this week · Jobs beat: +115K vs 60K forecast · '
        'US-Iran ceasefire holding · AI capex boom continues · '
        'Oil ~$101/bbl · Fed rate decision: next meeting June 17'
        '</div>',
        unsafe_allow_html=True)

    st.markdown("---")

    # ── market chart with time range selector ─────────────────────────────────
    st.subheader("📊 Market Indices — Performance Chart")

    ctrl1, ctrl2, ctrl3 = st.columns([2,2,3])
    with ctrl1:
        time_range = st.segmented_control(
            "Range", ["1W","1M","6M","1Y","All"],
            default="6M", label_visibility="collapsed")
    with ctrl2:
        indices = st.multiselect(
            "Indices", ["S&P 500","Nasdaq-100","Dow Jones"],
            default=["S&P 500","Nasdaq-100"],
            label_visibility="collapsed")

    tr = time_range or "6M"
    data = CHART_DATA[tr]

    key_map = {"S&P 500":"spy","Nasdaq-100":"qqq","Dow Jones":"dia"}
    selected_keys = [key_map[i] for i in indices if i in key_map]

    fig = go.Figure()
    for key in selected_keys:
        color, label = INDEX_COLORS[key]
        fig.add_trace(go.Scatter(
            x=data["labels"], y=data[key],
            name=label, mode="lines",
            fill="tozeroy" if len(selected_keys)==1 else "none",
            line=dict(color=color, width=2.5),
            fillcolor=f"rgba{tuple(list(bytes.fromhex(color[1:])) + [20])}".replace("(","rgba(") if len(selected_keys)==1 else None,
        ))

    fig.update_layout(
        height=280, margin=dict(l=0,r=0,t=8,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(128,128,128,0.12)", tickprefix="$",
                   tickformat=",", color="rgba(128,128,128,0.7)"),
        xaxis=dict(gridcolor="rgba(128,128,128,0.12)", color="rgba(128,128,128,0.7)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── top buy / sell lists ──────────────────────────────────────────────────
    col_buy, col_sell = st.columns(2)

    with col_buy:
        st.subheader("🟢 Top 10 — Buy signals")
        rows_html = ""
        for s in TOP_BUYS:
            p, chg, chg_col, live = price_display(s["ticker"], prices)
            rows_html += _stock_row(s["ticker"], s["name"], s["signal"], p, chg, chg_col, live)
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.04);border:1px solid rgba(128,128,128,0.14);'
            f'border-radius:16px;padding:0.25rem 1rem;position:relative;overflow:hidden;">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;'
            f'background:linear-gradient(90deg,#1D9E75,#378ADD);opacity:0.5;border-radius:16px 16px 0 0;"></div>'
            f'{rows_html}</div>',
            unsafe_allow_html=True)

    with col_sell:
        st.subheader("🔴 Top 10 — Sell / Avoid")
        rows_html = ""
        for s in TOP_SELLS:
            p, chg, chg_col, live = price_display(s["ticker"], prices)
            rows_html += _stock_row(s["ticker"], s["name"], s["signal"], p, chg, chg_col, live)
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.04);border:1px solid rgba(128,128,128,0.14);'
            f'border-radius:16px;padding:0.25rem 1rem;position:relative;overflow:hidden;">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;'
            f'background:linear-gradient(90deg,#D85A30,#BA7517);opacity:0.5;border-radius:16px 16px 0 0;"></div>'
            f'{rows_html}</div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # ── AI advisor — general market recommendations ───────────────────────────
    st.subheader("🤖 AI Advisor — Market Recommendations")
    st.caption("General recommendations based on current market conditions — suitable for any investor.")

    recs = [
        ("VOO / SPY",  "S&P 500 Index ETFs",       "Strong Buy",  "#1D9E75",
         "The S&P 500 is on its 6th consecutive winning week and just hit an all-time high at 7,399. "
         "For long-term investors, dollar-cost averaging into a broad index ETF remains the single "
         "best risk-adjusted strategy regardless of market timing."),
        ("NVDA",       "Nvidia",                    "Buy",         "#378ADD",
         "AI infrastructure capex is hitting record levels. Nvidia holds 80%+ of the AI chip market "
         "and is partnering with Corning on new optical manufacturing facilities. "
         "Pullbacks toward $200 are strong entry points for long-term holders."),
        ("AVGO",       "Broadcom",                  "Buy",         "#378ADD",
         "Custom AI chip demand from Google and Meta is accelerating. Broadcom is in talks for a "
         "record $35B private credit deal tied to OpenAI chip supply, signalling massive growth ahead. "
         "Less volatile than NVDA with a growing dividend."),
        ("GLD",        "SPDR Gold ETF",             "Add / Hedge", "#BA7517",
         "With US-Iran tensions ongoing and oil above $100/barrel, gold is the strongest macro hedge "
         "available. Economists are warning of recession risk from the oil shock — allocating 5–10% "
         "to gold protects the portfolio in a worst-case scenario."),
        ("NET / ZS",   "Cloudflare / Zscaler",      "Watch",       "#888780",
         "Cloudflare dropped 14% after announcing 1,100 layoffs despite strong earnings, blaming AI "
         "for operational efficiency gains. This creates a potential dip-buying opportunity for "
         "investors bullish on cybersecurity long-term."),
    ]

    for ticker, name, action, accent, reason in recs:
        inner = (
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
            f'<div><span style="font-weight:700;font-size:1rem">{ticker}</span>'
            f'<span style="opacity:0.5;font-size:0.8rem;margin-left:8px">{name}</span></div>'
            f'{_badge(action)}</div>'
            f'<div style="font-size:0.84rem;opacity:0.75;line-height:1.55">{reason}</div>'
        )
        st.markdown(_card(inner, accent), unsafe_allow_html=True)

    # ── sector sentiment ──────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📊 Sector sentiment")
    sectors = [
        ("Technology",   82, "#1D9E75", "Bullish"),
        ("Healthcare",   65, "#1D9E75", "Bullish"),
        ("Defense",      72, "#1D9E75", "Bullish"),
        ("Energy",       58, "#BA7517", "Neutral"),
        ("Financials",   54, "#BA7517", "Neutral"),
        ("Consumer",     38, "#D85A30", "Bearish"),
        ("Real Estate",  33, "#D85A30", "Bearish"),
        ("Utilities",    45, "#BA7517", "Neutral"),
    ]
    c1,c2 = st.columns(2)
    for i,(sector,pct,color,label) in enumerate(sectors):
        col = c1 if i%2==0 else c2
        col.markdown(
            f'<div style="margin-bottom:12px">'
            f'<div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:5px">'
            f'<span style="opacity:0.75">{sector}</span>'
            f'<span style="color:{color};font-weight:700">{label} {pct}%</span></div>'
            f'<div class="sent-track"><div class="sent-fill" style="width:{pct}%;background:{color}"></div></div>'
            f'</div>',
            unsafe_allow_html=True)
