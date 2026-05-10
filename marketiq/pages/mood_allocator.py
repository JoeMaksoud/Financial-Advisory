import streamlit as st
import plotly.graph_objects as go
from data.stock_data import MOOD_PROFILES, STOCKS


MOOD_META = {
    "Ambitious": {
        "icon": "🔥",
        "tag": "High risk / High reward",
        "desc": "I am willing to take risks for higher returns",
        "color": "#D85A30",
        "glow": "rgba(216,90,48,0.18)",
        "border_sel": "rgba(216,90,48,0.7)",
        "border_unsel": "rgba(128,128,128,0.18)",
    },
    "Cautious": {
        "icon": "🛡️",
        "tag": "Low risk / Stable returns",
        "desc": "I want steady growth with minimal risk",
        "color": "#1D9E75",
        "glow": "rgba(29,158,117,0.18)",
        "border_sel": "rgba(29,158,117,0.7)",
        "border_unsel": "rgba(128,128,128,0.18)",
    },
    "Curious": {
        "icon": "🔭",
        "tag": "Balanced risk",
        "desc": "Show me a mix of bold and safe plays",
        "color": "#378ADD",
        "glow": "rgba(55,138,221,0.18)",
        "border_sel": "rgba(55,138,221,0.7)",
        "border_unsel": "rgba(128,128,128,0.18)",
    },
}


def _mood_card(mood_name, meta, selected):
    is_sel = selected == mood_name
    border  = meta["border_sel"]  if is_sel else meta["border_unsel"]
    bg      = meta["glow"]        if is_sel else "rgba(128,128,128,0.05)"
    shadow  = f"0 0 20px {meta['glow']}, 0 4px 16px rgba(0,0,0,0.12)" if is_sel else "0 2px 8px rgba(0,0,0,0.06)"
    accent_bar = f'<div style="position:absolute;top:0;left:0;right:0;height:3px;background:{meta["color"]};border-radius:14px 14px 0 0;opacity:{"1" if is_sel else "0.3"}"></div>' if is_sel else ""
    check = f'<span style="position:absolute;top:12px;right:12px;background:{meta["color"]};color:#fff;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:0.7rem;font-weight:700">✓</span>' if is_sel else ""

    return (
        f'<div style="position:relative;background:{bg};border:2px solid {border};'
        f'border-radius:14px;padding:18px 16px 14px;margin-bottom:10px;'
        f'box-shadow:{shadow};transition:all 0.2s;overflow:hidden;min-height:140px;">'
        f'{accent_bar}{check}'
        f'<div style="font-size:1.6rem;margin-bottom:8px">{meta["icon"]}</div>'
        f'<div style="font-weight:700;font-size:0.95rem;margin-bottom:4px">{mood_name}</div>'
        f'<div style="font-size:0.8rem;opacity:0.65;line-height:1.45;margin-bottom:10px">{meta["desc"]}</div>'
        f'<span style="font-size:0.7rem;font-weight:700;color:{meta["color"]};'
        f'background:{"rgba(255,255,255,0.12)" if is_sel else "rgba(128,128,128,0.08)"};'
        f'border:1px solid {meta["color"]};padding:2px 9px;border-radius:20px;">{meta["tag"]}</span>'
        f'</div>'
    )


def show():
    st.markdown('<h2 style="font-size:1.4rem;font-weight:500;margin-bottom:4px">🎯 My Investment Plan</h2>', unsafe_allow_html=True)
    st.caption("Tell us how you feel today and how much you want to invest — we'll build your plan.")
    st.markdown("---")

    st.subheader("How do you feel today?")
    selected_mood = st.session_state.get("mood", None)

    cols = st.columns(3)
    for col, mood_name in zip(cols, MOOD_META):
        meta = MOOD_META[mood_name]
        with col:
            st.markdown(_mood_card(mood_name, meta, selected_mood), unsafe_allow_html=True)
            btn_label = f"✓ {mood_name} selected" if selected_mood == mood_name else f"Select {mood_name}"
            if st.button(btn_label, key=f"mood_{mood_name}", use_container_width=True):
                st.session_state["mood"] = mood_name
                st.rerun()

    st.markdown("---")

    amount = st.number_input(
        "How much do you want to invest today? ($)",
        min_value=50.0, max_value=1_000_000.0,
        value=500.0, step=50.0, format="%.0f",
    )

    generate = st.button("Build my investment plan", type="primary", use_container_width=True)

    mood = st.session_state.get("mood", None)

    if generate and not mood:
        st.warning("Please select a mood above first.")
        return

    if generate and mood and amount:
        profile = MOOD_PROFILES[mood]
        meta    = MOOD_META[mood]

        st.markdown("---")
        st.subheader(f"{meta['icon']} Your {mood} plan — ${amount:,.0f}")
        st.caption(profile["description"])

        m1, m2, m3 = st.columns(3)
        m1.metric("Expected return",   profile["expected"])
        m2.metric("Suggested horizon", profile["horizon"])
        m3.metric("Volatility",        profile["volatility"])

        st.markdown("&nbsp;")

        chart_col, table_col = st.columns([1, 1.6])

        colors = ["#1D9E75","#378ADD","#D85A30","#BA7517","#7F77DD","#888780"]
        with chart_col:
            fig = go.Figure(go.Pie(
                labels=[s["ticker"] for s in profile["stocks"]],
                values=[s["pct"]    for s in profile["stocks"]],
                hole=0.52,
                marker_colors=colors,
                textinfo="label+percent",
                textfont_size=12,
            ))
            fig.update_layout(
                height=280, margin=dict(l=0,r=0,t=8,b=0),
                showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

        with table_col:
            risk_styles = {
                "Low":    "background:rgba(29,158,117,0.15);color:#1D9E75;border:1px solid rgba(29,158,117,0.3)",
                "Medium": "background:rgba(186,117,23,0.15);color:#BA7517;border:1px solid rgba(186,117,23,0.3)",
                "High":   "background:rgba(216,90,48,0.15);color:#D85A30;border:1px solid rgba(216,90,48,0.3)",
            }
            for stock in profile["stocks"]:
                dollars  = amount * stock["pct"] / 100
                rs       = risk_styles.get(stock["risk"], "")
                st.markdown(
                    f'<div style="background:rgba(128,128,128,0.06);border:1px solid rgba(128,128,128,0.13);'
                    f'border-radius:12px;padding:10px 14px;margin-bottom:8px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'
                    f'  <span style="font-weight:700;font-size:0.95rem">{stock["ticker"]}</span>'
                    f'  <div style="display:flex;gap:8px;align-items:center">'
                    f'    <span style="{rs};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:600">{stock["risk"]} risk</span>'
                    f'    <span style="font-weight:700;color:{meta["color"]};font-size:1rem">${dollars:,.0f}</span>'
                    f'    <span style="font-size:0.75rem;opacity:0.45">{stock["pct"]}%</span>'
                    f'  </div>'
                    f'</div>'
                    f'<div style="font-size:0.78rem;opacity:0.6;line-height:1.45">{stock["rationale"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.caption("⚠️ Not financial advice. Past performance does not guarantee future results.")
