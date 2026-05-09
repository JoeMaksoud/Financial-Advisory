import streamlit as st
import plotly.graph_objects as go
from data.stock_data import MOOD_PROFILES, STOCKS


def show():
    st.title("🎯 Mood Allocator")
    st.caption("Tell us how you feel today and how much you want to invest — we'll build your plan.")

    st.markdown("---")

    # ── mood selector ─────────────────────────────────────────────────────────
    st.subheader("How do you feel today?")
    mood_col1, mood_col2, mood_col3 = st.columns(3)

    mood_meta = {
        "Ambitious": {
            "icon": "🔥",
            "tag": "High risk / High reward",
            "desc": "I am willing to take risks for higher returns",
            "border": "#D85A30",
        },
        "Cautious": {
            "icon": "🛡️",
            "tag": "Low risk / Stable returns",
            "desc": "I want steady growth with minimal risk",
            "border": "#1D9E75",
        },
        "Curious": {
            "icon": "🔭",
            "tag": "Balanced risk",
            "desc": "Show me a mix of bold and safe plays",
            "border": "#378ADD",
        },
    }

    selected_mood = st.session_state.get("mood", None)

    for col, mood_name in zip([mood_col1, mood_col2, mood_col3], mood_meta):
        meta = mood_meta[mood_name]
        border = meta["border"] if selected_mood == mood_name else "#e5e7eb"
        bg = f"rgba({','.join(str(int(c*255)) for c in _hex_to_rgb(meta['border']))},0.06)" if selected_mood == mood_name else "#fff"
        with col:
            st.markdown(
                f"""<div style="border:2px solid {border};background:{bg};border-radius:12px;padding:16px;margin-bottom:8px">
                  <div style="font-size:1.4rem;margin-bottom:6px">{meta['icon']}</div>
                  <div style="font-weight:600;font-size:0.95rem;margin-bottom:4px">{mood_name}</div>
                  <div style="font-size:0.8rem;color:#555;margin-bottom:8px">{meta['desc']}</div>
                  <span style="font-size:0.7rem;font-weight:600;color:{meta['border']}">{meta['tag']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"Select {mood_name}", key=f"mood_{mood_name}", use_container_width=True):
                st.session_state["mood"] = mood_name
                st.rerun()

    st.markdown("---")

    # ── amount input ──────────────────────────────────────────────────────────
    amount = st.number_input(
        "How much do you want to invest today? ($)",
        min_value=50.0,
        max_value=1_000_000.0,
        value=500.0,
        step=50.0,
        format="%.0f",
    )

    generate = st.button("Build my investment plan", type="primary", use_container_width=True)

    # ── results ───────────────────────────────────────────────────────────────
    mood = st.session_state.get("mood", None)

    if generate and mood and amount:
        profile = MOOD_PROFILES[mood]

        st.markdown("---")
        st.subheader(f"{mood_meta[mood]['icon']} Your {mood} plan — ${amount:,.0f}")
        st.caption(profile["description"])

        # summary metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Expected return", profile["expected"])
        m2.metric("Suggested horizon", profile["horizon"])
        m3.metric("Volatility", profile["volatility"])

        st.markdown("&nbsp;")

        # pie chart + table
        chart_col, table_col = st.columns([1, 1.6])

        labels = [s["ticker"] for s in profile["stocks"]]
        values = [s["pct"] for s in profile["stocks"]]
        colors = ["#1D9E75", "#378ADD", "#D85A30", "#BA7517", "#7F77DD", "#888780"]

        with chart_col:
            fig = go.Figure(go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker_colors=colors,
                textinfo="label+percent",
                textfont_size=12,
            ))
            fig.update_layout(
                height=280,
                margin=dict(l=0, r=0, t=8, b=0),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

        with table_col:
            for stock in profile["stocks"]:
                dollars = amount * stock["pct"] / 100
                risk_colors = {
                    "Low":    ("#d1fae5", "#065f46"),
                    "Medium": ("#fef3c7", "#92400e"),
                    "High":   ("#fee2e2", "#991b1b"),
                }
                rbg, rfg = risk_colors.get(stock["risk"], ("#f3f4f6", "#374151"))
                st.markdown(
                    f"""<div style="background:#f9fafb;border-radius:10px;padding:10px 12px;margin-bottom:8px">
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                        <span style="font-weight:700">{stock['ticker']}</span>
                        <div style="display:flex;gap:8px;align-items:center">
                          <span style="background:{rbg};color:{rfg};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:600">{stock['risk']} risk</span>
                          <span style="font-weight:700;color:{profile['color']}">${dollars:,.0f}</span>
                          <span style="font-size:0.75rem;color:#888">{stock['pct']}%</span>
                        </div>
                      </div>
                      <div style="font-size:0.78rem;color:#555;line-height:1.45">{stock['rationale']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.caption(
            "⚠️ Not financial advice. Allocations are based on current market signals and your "
            "selected risk profile. Past performance does not guarantee future results."
        )

    elif generate and not mood:
        st.warning("Please select a mood first.")


def _hex_to_rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
