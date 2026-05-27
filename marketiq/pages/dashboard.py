import streamlit as st
import plotly.graph_objects as go
from data.stock_data import ETF_BUYS, ETF_SELLS, STOCK_BUYS, STOCK_SELLS, SECTOR_SENTIMENT, ADVISOR_PICKS
from data.live_prices import get_prices, price_display, format_last_updated

CHART_DATA = {
    "1W": {
        "labels": ["Mon May 4", "Tue May 5", "Wed May 6", "Thu May 7", "Fri May 8"],
        "spy":    [658.2, 662.5, 672.8, 670.1, 676.4],
        "qqq":    [472.1, 477.3, 486.9, 484.2, 490.8],
        "dia":    [480.3, 482.1, 487.6, 485.9, 488.2],
    },
    "1M": {
        "labels": ["Apr 7", "Apr 14", "Apr 21", "Apr 28", "May 5", "May 8"],
        "spy":    [601.4, 628.3, 643.7, 657.2, 668.9, 676.4],
        "qqq":    [428.6, 450.2, 461.8, 472.5, 482.1, 490.8],
        "dia":    [456.2, 468.4, 475.6, 480.1, 485.3, 488.2],
    },
    "6M": {
        "labels": ["Nov '25", "Dec '25", "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26"],
        "spy":    [582.0, 591.0, 578.0, 565.0, 521.0, 618.0, 676.4],
        "qqq":    [502.3, 512.1, 498.4, 483.2, 441.7, 468.3, 490.8],
        "dia":    [444.2, 452.1, 445.8, 438.3, 421.6, 471.4, 488.2],
    },
    "1Y": {
        "labels": ["May '25", "Jul '25", "Sep '25", "Nov '25", "Jan '26", "Mar '26", "May '26"],
        "spy":    [532.0, 555.0, 543.0, 582.0, 578.0, 521.0, 676.4],
        "qqq":    [444.2, 468.1, 457.3, 502.3, 498.4, 441.7, 490.8],
        "dia":    [398.1, 416.3, 408.7, 444.2, 445.8, 421.6, 488.2],
    },
    "All": {
        "labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
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
        "Strong Buy": "badge-buy", "Buy": "badge-buy", "Accumulate": "badge-buy",
        "Watch / Accumulate": "badge-buy", "Watch": "badge-watch",
        "Reduce": "badge-sell", "Avoid": "badge-sell", "Trim": "badge-sell",
        "Hold only": "badge-hold", "Hold / Trim": "badge-hold",
    }.get(signal, "badge-hold")
    return f'<span class="{cls}">{signal}</span>'


def _score_bar(score):
    color = "#1D9E75" if score >= 75 else "#BA7517" if score >= 50 else "#D85A30"
    return (
        f'<div style="display:flex;align-items:center;gap:6px;margin-top:4px">'
        f'<div style="flex:1;height:4px;background:rgba(128,128,128,0.15);border-radius:2px;overflow:hidden">'
        f'<div style="width:{score}%;height:100%;background:{color};border-radius:2px"></div></div>'
        f'<span style="font-size:10px;font-weight:600;color:{color}">{score}/100</span>'
        f'</div>'
    )


def _rec_card(item, is_etf=True):
    ticker = item["ticker"]
    name   = item["name"]
    signal = item["signal"]
    score  = item.get("score", 50)
    thesis = item["thesis"]
    factors = item.get("factors", {})
    region = item.get("region", "")

    price_str = f'${item["price"]:,.2f}'
    chg = item["chg"]
    chg_str = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"
    chg_color = "#1D9E75" if chg >= 0 else "#D85A30"

    factors_html = ""
    for k, v in factors.items():
        col = "#1D9E75" if "↑" in str(v) else "#D85A30" if "↓" in str(v) else "inherit"
        factors_html += (
            f'<div style="display:flex;justify-content:space-between;'
            f'font-size:0.72rem;padding:3px 0;border-bottom:0.5px solid rgba(128,128,128,0.08)">'
            f'<span style="opacity:0.55">{k}</span>'
            f'<span style="font-weight:500;color:{col}">{v}</span></div>'
        )

    region_html = f'<span style="font-size:10px;opacity:0.45;margin-left:4px">{region}</span>' if region else ""

    return (
        f'<div style="background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.14);'
        f'border-radius:14px;padding:12px 14px;margin-bottom:10px;transition:box-shadow 0.2s">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">'
        f'  <div><span style="font-weight:700;font-size:0.95rem">{ticker}</span>{region_html}'
        f'  <div style="font-size:0.75rem;opacity:0.5;margin-top:1px">{name}</div></div>'
        f'  <div style="text-align:right">'
        f'    <div style="font-weight:600;font-size:0.9rem">{price_str}</div>'
        f'    <div style="font-size:0.72rem;color:{chg_color}">{chg_str}</div>'
        f'  </div>'
        f'</div>'
        f'{_badge(signal)}'
        f'{_score_bar(score)}'
        f'<div style="font-size:0.78rem;opacity:0.65;line-height:1.5;margin:8px 0 6px">{thesis}</div>'
        f'{factors_html}'
        f'</div>'
    )


def _stock_rec_card(item):
    ticker = item["ticker"]
    name   = item["name"]
    signal = item["signal"]
    score  = item.get("score", 50)
    thesis = item["thesis"]
    funds  = item.get("fundamentals", {})
    region = item.get("region", "")
    sector = item.get("sector", "")
    horizon = item.get("horizon", "")
    risks   = item.get("risks", "")

    price_str = f'${item["price"]:,.2f}'
    chg = item["chg"]
    chg_str = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"
    chg_color = "#1D9E75" if chg >= 0 else "#D85A30"

    funds_html = ""
    for k, v in funds.items():
        col = "#1D9E75" if ("+" in str(v) and "↓" not in str(v)) or "↑" in str(v) else \
              "#D85A30" if ("-" in str(v) and "target" not in k.lower()) or "↓" in str(v) else "inherit"
        funds_html += (
            f'<div style="display:flex;justify-content:space-between;'
            f'font-size:0.72rem;padding:3px 0;border-bottom:0.5px solid rgba(128,128,128,0.08)">'
            f'<span style="opacity:0.5">{k}</span>'
            f'<span style="font-weight:500;color:{col};text-align:right;max-width:55%">{v}</span></div>'
        )

    risks_html = (
        f'<div style="margin-top:6px;font-size:0.72rem;background:rgba(216,90,48,0.07);'
        f'border-radius:8px;padding:5px 8px;opacity:0.75">'
        f'⚠️ {risks}</div>'
    ) if risks else ""

    horizon_html = (
        f'<div style="margin-top:6px;font-size:0.71rem;opacity:0.45">⏱ {horizon}</div>'
    ) if horizon else ""

    return (
        f'<div style="background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.14);'
        f'border-radius:14px;padding:12px 14px;margin-bottom:10px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">'
        f'  <div>'
        f'    <span style="font-weight:700;font-size:0.95rem">{ticker}</span>'
        f'    <span style="font-size:10px;opacity:0.4;margin-left:5px">{region}</span>'
        f'    <div style="font-size:0.75rem;opacity:0.5;margin-top:1px">{name} · {sector}</div>'
        f'  </div>'
        f'  <div style="text-align:right">'
        f'    <div style="font-weight:600;font-size:0.9rem">{price_str}</div>'
        f'    <div style="font-size:0.72rem;color:{chg_color}">{chg_str}</div>'
        f'  </div>'
        f'</div>'
        f'{_badge(signal)}'
        f'{_score_bar(score)}'
        f'<div style="font-size:0.78rem;opacity:0.65;line-height:1.5;margin:8px 0 6px">{thesis}</div>'
        f'{funds_html}'
        f'{risks_html}'
        f'{horizon_html}'
        f'</div>'
    )


def show():
    st.markdown('<h2 style="font-size:1.5rem;font-weight:600;letter-spacing:-0.3px;margin-bottom:4px">Market Overview</h2>', unsafe_allow_html=True)

    # live prices
    all_tickers = ["SPY", "QQQ", "DIA"] + \
                  [s["ticker"] for s in ETF_BUYS + ETF_SELLS] + \
                  [s["ticker"] for s in STOCK_BUYS + STOCK_SELLS]
    prices = get_prices(list(set(all_tickers)))
    any_live = any(v.get("status") == "live" for v in prices.values())

    col_s, col_r = st.columns([4, 1])
    with col_s:
        if any_live:
            st.caption(f"🟢 Live data via Yahoo Finance · {format_last_updated()} · Auto-refreshes every 5 min")
        else:
            st.caption("🕐 Markets closed — showing last known prices · Will update when markets open")
    with col_r:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    # ── Top metrics ───────────────────────────────────────────────────────────
    spy_p, spy_c, spy_col, spy_lbl, spy_icon = price_display("SPY", prices)
    qqq_p, qqq_c, qqq_col, qqq_lbl, qqq_icon = price_display("QQQ", prices)
    dia_p, dia_c, dia_col, dia_lbl, dia_icon = price_display("DIA", prices)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("S&P 500 (SPY)",    f"{spy_icon} {spy_p}", spy_c)
    c2.metric("Nasdaq-100 (QQQ)", f"{qqq_icon} {qqq_p}", qqq_c)
    c3.metric("Dow Jones (DIA)",  f"{dia_icon} {dia_p}", dia_c)
    c4.metric("Market Trend",  "↑ Bullish",     "6th winning week")
    c5.metric("Fear & Greed",  "68 — Greed",    "↑ from 58 last wk")
    c6.metric("VIX Volatility", "~16",           "Low — calm market")

    st.markdown(
        '<div style="background:rgba(29,158,117,0.07);border:0.5px solid rgba(29,158,117,0.2);'
        'border-radius:12px;padding:10px 16px;margin:14px 0;font-size:0.82rem;opacity:0.85">'
        '📰 <b>Market pulse (May 2026):</b> S&P 500 at record 7,399 · Nasdaq +4.5% this week · '
        'Jobs +115K vs 60K forecast · US-Iran ceasefire holding · AI capex boom continues · '
        'Oil ~$101/bbl · Fed rate decision: June 17'
        '</div>',
        unsafe_allow_html=True)

    st.markdown("---")

    # ── Chart ─────────────────────────────────────────────────────────────────
    st.subheader("📊 Market Indices — Performance Chart")
    ctrl1, ctrl2 = st.columns([2, 3])
    with ctrl1:
        tr = st.segmented_control("Range", ["1W", "1M", "6M", "1Y", "All"], default="6M", label_visibility="collapsed")
    with ctrl2:
        indices = st.multiselect("Indices", ["S&P 500", "Nasdaq-100", "Dow Jones"],
                                 default=["S&P 500", "Nasdaq-100"], label_visibility="collapsed")

    tr = tr or "6M"
    data = CHART_DATA[tr]
    key_map = {"S&P 500": "spy", "Nasdaq-100": "qqq", "Dow Jones": "dia"}
    selected_keys = [key_map[i] for i in indices if i in key_map]

    fig = go.Figure()
    for key in selected_keys:
        color, label = INDEX_COLORS[key]
        fig.add_trace(go.Scatter(
            x=data["labels"], y=data[key], name=label, mode="lines",
            fill="tozeroy" if len(selected_keys) == 1 else "none",
            line=dict(color=color, width=2.5),
            fillcolor=f"rgba(29,158,117,0.07)" if len(selected_keys) == 1 else None,
        ))
    fig.update_layout(
        height=280, margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(128,128,128,0.12)", tickprefix="$", tickformat=",",
                   color="rgba(128,128,128,0.7)"),
        xaxis=dict(gridcolor="rgba(128,128,128,0.12)", color="rgba(128,128,128,0.7)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── ETF Recommendations ───────────────────────────────────────────────────
    st.subheader("📦 ETF Recommendations")
    st.caption("ETFs reduce individual stock risk while capturing sector and index growth. Recommended as the foundation of any portfolio.")

    col_etf_buy, col_etf_sell = st.columns(2)

    with col_etf_buy:
        st.markdown("#### 🟢 ETFs — Buy / Accumulate")
        for etf in ETF_BUYS:
            st.markdown(_rec_card(etf, is_etf=True), unsafe_allow_html=True)

    with col_etf_sell:
        st.markdown("#### 🔴 ETFs — Reduce / Avoid")
        for etf in ETF_SELLS:
            st.markdown(_rec_card(etf, is_etf=True), unsafe_allow_html=True)

    st.markdown("---")

    # ── Stock Recommendations ─────────────────────────────────────────────────
    st.subheader("📈 Individual Stock Recommendations")
    st.caption("Fundamentals-based picks covering US and international markets. Each recommendation includes revenue trends, analyst consensus, price targets, and key risks — not just today's price.")

    col_buy, col_sell = st.columns(2)

    with col_buy:
        st.markdown("#### 🟢 Stocks — Buy signals")
        for s in STOCK_BUYS:
            st.markdown(_stock_rec_card(s), unsafe_allow_html=True)

    with col_sell:
        st.markdown("#### 🔴 Stocks — Sell / Avoid")
        for s in STOCK_SELLS:
            st.markdown(_stock_rec_card(s), unsafe_allow_html=True)

    st.markdown("---")

    # ── AI Advisor ────────────────────────────────────────────────────────────
    st.subheader("🤖 AI Advisor — Portfolio Recommendations")
    st.caption("Holistic recommendations for any investor, based on current market conditions, macro trends, and long-term fundamentals.")

    for pick in ADVISOR_PICKS:
        accent = pick["accent"]
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.06);border:0.5px solid rgba(128,128,128,0.15);'
            f'border-radius:16px;padding:1rem 1.25rem;margin-bottom:0.75rem;position:relative;overflow:hidden;">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;background:{accent};'
            f'border-radius:16px 16px 0 0;opacity:0.8"></div>'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
            f'<div><span style="font-weight:700;font-size:1rem">{pick["ticker"]}</span>'
            f'<span style="opacity:0.5;font-size:0.8rem;margin-left:8px">{pick["name"]}</span></div>'
            f'{_badge(pick["action"])}'
            f'</div>'
            f'<div style="font-size:0.84rem;opacity:0.75;line-height:1.55;margin-bottom:8px">{pick["thesis"]}</div>'
            f'<div style="display:flex;gap:20px;font-size:0.72rem;opacity:0.5">'
            f'<span>Horizon: <b style="opacity:1">{pick["horizon"]}</b></span>'
            f'<span>Allocation: <b style="opacity:1">{pick["allocation"]}</b></span>'
            f'</div></div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # ── Sector Sentiment ──────────────────────────────────────────────────────
    st.subheader("📊 Sector Sentiment & ETF Playbook")
    st.caption("Each sector signal comes with a specific ETF to buy and individual stocks to consider.")

    for s in SECTOR_SENTIMENT:
        color = s["color"]
        score = s["score"]
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.13);'
            f'border-radius:14px;padding:12px 14px;margin-bottom:8px;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
            f'  <div style="display:flex;align-items:center;gap:10px">'
            f'    <span style="font-weight:600;font-size:0.9rem">{s["sector"]}</span>'
            f'    <span style="font-size:10px;font-weight:600;color:{color};background:rgba(128,128,128,0.08);'
            f'    padding:1px 8px;border-radius:10px">{s["direction"]}</span>'
            f'  </div>'
            f'  <span style="font-size:11px;font-weight:600;color:{color}">{score}/100</span>'
            f'</div>'
            f'<div class="sent-track" style="margin-bottom:8px">'
            f'  <div class="sent-fill" style="width:{score}%;background:{color}"></div>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:0.75rem">'
            f'  <div><span style="opacity:0.45">ETF play</span><br>'
            f'    <span style="font-weight:600;color:{color}">{s["etf"]}</span></div>'
            f'  <div><span style="opacity:0.45">Stock picks</span><br>'
            f'    <span style="font-weight:600">{s["stock_pick"]}</span></div>'
            f'  <div><span style="opacity:0.45">Why</span><br>'
            f'    <span style="opacity:0.7">{s["etf_reason"]}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True)
