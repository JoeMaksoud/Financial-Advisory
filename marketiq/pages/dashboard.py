import streamlit as st
import plotly.graph_objects as go
from data.stock_data import TOP_BUYS, TOP_SELLS

_SPX = [5820, 5910, 5780, 5650, 5210, 5480, 5631]
_LABELS = ["Nov '25", "Dec '25", "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26"]


def _badge(signal: str) -> str:
    cls = {
        "Strong Buy": "badge-buy", "Buy": "badge-buy", "Add more": "badge-buy",
        "Keep DCA": "badge-buy",
        "Reduce": "badge-sell", "Sell": "badge-sell", "Avoid": "badge-sell",
        "Hold only": "badge-hold", "Watch": "badge-watch",
    }.get(signal, "badge-hold")
    return f'<span class="{cls}">{signal}</span>'


def _chg_color(chg: float) -> str:
    return "#1D9E75" if chg >= 0 else "#D85A30"


def show():
    st.title("📈 MarketIQ Dashboard")
    st.caption("Live market intelligence — May 2026")

    # ── top metrics ──────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("VOO", "$548.20", "+0.82%")
    c2.metric("S&P 500", "5,631", "+0.76%")
    c3.metric("Market Mood", "Cautious Bull", "67/100")
    c4.metric("Fear & Greed", "58", "Greed zone")
    c5.metric("Your Signal", "Accumulate", "DCA this month")

    st.markdown("---")

    # ── S&P chart ────────────────────────────────────────────────────────────
    st.subheader("S&P 500 — 6-month trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=_LABELS, y=_SPX,
        mode="lines", fill="tozeroy",
        line=dict(color="#1D9E75", width=2),
        fillcolor="rgba(29,158,117,0.08)",
        name="S&P 500",
    ))
    fig.update_layout(
        height=220, margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f0f0", tickprefix="$", tickformat=","),
        xaxis=dict(gridcolor="#f0f0f0"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── buy / sell lists ─────────────────────────────────────────────────────
    col_buy, col_sell = st.columns(2)

    with col_buy:
        st.subheader("🟢 Top 10 — Buy signals")
        for s in TOP_BUYS:
            chg = s["chg"]
            chg_str = f"+{chg}%" if chg >= 0 else f"{chg}%"
            st.markdown(
                f"""<div style="display:flex;justify-content:space-between;align-items:center;
                    padding:8px 0;border-bottom:1px solid #f0f0f0;">
                  <div>
                    <span style="font-weight:600;font-size:0.9rem">{s['ticker']}</span>
                    &nbsp;{_badge(s['signal'])}
                    <div style="font-size:0.75rem;color:#888;margin-top:2px">{s['name']}</div>
                  </div>
                  <div style="text-align:right">
                    <div style="font-weight:600">${s['price']:,.0f}</div>
                    <div style="font-size:0.75rem;color:{_chg_color(chg)}">{chg_str}</div>
                  </div>
                </div>""",
                unsafe_allow_html=True,
            )

    with col_sell:
        st.subheader("🔴 Top 10 — Sell / Avoid")
        for s in TOP_SELLS:
            chg = s["chg"]
            chg_str = f"+{chg}%" if chg >= 0 else f"{chg}%"
            st.markdown(
                f"""<div style="display:flex;justify-content:space-between;align-items:center;
                    padding:8px 0;border-bottom:1px solid #f0f0f0;">
                  <div>
                    <span style="font-weight:600;font-size:0.9rem">{s['ticker']}</span>
                    &nbsp;{_badge(s['signal'])}
                    <div style="font-size:0.75rem;color:#888;margin-top:2px">{s['name']}</div>
                  </div>
                  <div style="text-align:right">
                    <div style="font-weight:600">${s['price']:,.0f}</div>
                    <div style="font-size:0.75rem;color:{_chg_color(chg)}">{chg_str}</div>
                  </div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── AI recommendations ───────────────────────────────────────────────────
    st.subheader("🤖 AI Advisor — Personalized recommendations")
    recs = [
        ("VOO",   "Vanguard S&P 500 ETF",   "Buy / Add",
         "Continue your monthly DCA into VOO. Current geopolitical tension is creating "
         "short-term dips — historically, DCA investors who held through similar periods "
         "saw 18–24% gains over 3–5 years.",
         "3–5 yrs", "50–60% of monthly budget", "High"),
        ("MSFT",  "Microsoft",              "Buy",
         "AI infrastructure spending is accelerating. Azure + Copilot revenue beat estimates. "
         "Global enterprise cloud adoption is not slowing. A pullback to ~$415 would be an excellent entry.",
         "2–4 yrs", "15–20%", "High"),
        ("BRK.B", "Berkshire Hathaway B",   "Hold / Add",
         "Buffett's large cash position signals a defensive posture. Good as a hedge against "
         "market volatility, especially given current trade war uncertainty.",
         "3+ yrs", "10–15%", "Medium"),
    ]
    for ticker, name, action, reason, horizon, alloc, conviction in recs:
        badge_html = _badge(action)
        st.markdown(
            f"""<div class="rec-box">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px">
                <div>
                  <span style="font-weight:700;font-size:1rem">{ticker}</span>
                  <span style="color:#888;font-size:0.8rem;margin-left:8px">{name}</span>
                </div>
                {badge_html}
              </div>
              <div style="font-size:0.85rem;color:#374151;margin-bottom:8px">{reason}</div>
              <div style="display:flex;gap:20px;font-size:0.75rem;color:#888">
                <span>Hold: <b style="color:#111">{horizon}</b></span>
                <span>Allocation: <b style="color:#111">{alloc}</b></span>
                <span>Conviction: <b style="color:#111">{conviction}</b></span>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )

    # ── sentiment bars ───────────────────────────────────────────────────────
    st.markdown("---")
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
        with col:
            col.markdown(
                f"""<div style="margin-bottom:10px">
                  <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px">
                    <span>{sector}</span>
                    <span style="color:{color};font-weight:600">{label} {pct}%</span>
                  </div>
                  <div style="background:#f0f0f0;border-radius:4px;height:6px">
                    <div style="background:{color};width:{pct}%;height:100%;border-radius:4px"></div>
                  </div>
                </div>""",
                unsafe_allow_html=True,
            )
