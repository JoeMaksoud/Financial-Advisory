import streamlit as st
import plotly.graph_objects as go

MOOD_META = {
    "Ambitious":{"icon":"🔥","tag":"High risk / High reward","desc":"Willing to take risks for higher returns","color":"#D85A30","glow":"rgba(216,90,48,0.15)","border":"rgba(216,90,48,0.6)"},
    "Cautious":{"icon":"🛡️","tag":"Low risk / Stable returns","desc":"Steady growth with minimal risk","color":"#1D9E75","glow":"rgba(29,158,117,0.15)","border":"rgba(29,158,117,0.6)"},
    "Curious":{"icon":"🔭","tag":"Balanced risk","desc":"Mix of bold and safe plays","color":"#378ADD","glow":"rgba(55,138,221,0.15)","border":"rgba(55,138,221,0.6)"},
}

PROFILES = {
    "Ambitious":{"expected":"18–35%/yr","horizon":"3–7 yrs","volatility":"High — 20–40% drawdowns possible","stocks":[
        {"ticker":"NVDA","pct":25,"risk":"High","rationale":"Dominant AI chip play. Highest upside in current cycle."},
        {"ticker":"SOXX","pct":20,"risk":"Mid","rationale":"Semiconductor ETF — AI chip demand structural, not cyclical."},
        {"ticker":"APP","pct":15,"risk":"High","rationale":"AppLovin — AI ad tech, EPS +180% YoY, most investors overlook it."},
        {"ticker":"META","pct":15,"risk":"High","rationale":"Ad revenue + AI. Highest ROIC of the Mag 7."},
        {"ticker":"MELI","pct":15,"risk":"Mid","rationale":"Amazon + PayPal of LatAm. 37% revenue growth, 220M users."},
        {"ticker":"ITA","pct":10,"risk":"Mid","rationale":"Defense ETF — NATO spending locked in 5+ years."},
    ]},
    "Cautious":{"expected":"8–14%/yr","horizon":"5–10 yrs","volatility":"Low — max ~12% drawdown","stocks":[
        {"ticker":"VOO","pct":40,"risk":"Low","rationale":"Core S&P 500 ETF. 10.7% avg annual return over 20 years. DCA monthly."},
        {"ticker":"SCHD","pct":20,"risk":"Low","rationale":"High-quality dividend growers. 3.5% yield. Rate-cut beneficiary."},
        {"ticker":"MSFT","pct":15,"risk":"Low","rationale":"Safest mega-cap. Cloud + AI moat. $75B free cash flow."},
        {"ticker":"VGK","pct":10,"risk":"Mid","rationale":"Europe ETF at historic discount to US. ECB cutting rates."},
        {"ticker":"GLD","pct":10,"risk":"Low","rationale":"Geopolitical hedge. 5–10% allocation as portfolio insurance."},
        {"ticker":"EWJ","pct":5,"risk":"Mid","rationale":"Japan at reform inflection. Buffett publicly buying Japanese stocks."},
    ]},
    "Curious":{"expected":"12–22%/yr","horizon":"3–7 yrs","volatility":"Medium — 10–20% drawdowns","stocks":[
        {"ticker":"VOO","pct":25,"risk":"Low","rationale":"Stable core. All macro tailwinds flow through here automatically."},
        {"ticker":"QQQM","pct":20,"risk":"Mid","rationale":"Nasdaq-100 — tech/AI upside with ETF diversification."},
        {"ticker":"SOXX","pct":15,"risk":"Mid","rationale":"Semiconductor ETF — cleaner AI play than individual names."},
        {"ticker":"ASML","pct":15,"risk":"Mid","rationale":"EUV monopoly. €36B backlog. Non-US diversification."},
        {"ticker":"SCHD","pct":15,"risk":"Low","rationale":"Dividend income stream. Balances growth volatility."},
        {"ticker":"VGK","pct":10,"risk":"Mid","rationale":"Europe at valuation discount. ECB rate cuts tailwind."},
    ]},
}

def show():
    st.markdown('<h2 style="font-size:1.5rem;font-weight:600;letter-spacing:-0.3px;margin-bottom:4px">My Investment Plan</h2>',unsafe_allow_html=True)
    st.caption("Select your risk appetite and investment amount — get a personalized allocation plan.")
    st.markdown("---")
    st.subheader("How do you feel today?")
    selected = st.session_state.get("mood",None)
    cols = st.columns(3)
    for col, mood_name in zip(cols, MOOD_META):
        meta = MOOD_META[mood_name]
        is_sel = selected == mood_name
        border = meta["border"] if is_sel else "rgba(128,128,128,0.18)"
        bg = meta["glow"] if is_sel else "rgba(128,128,128,0.05)"
        shadow = f"0 0 20px {meta['glow']}" if is_sel else "none"
        check = '<span style="position:absolute;top:10px;right:10px;background:'+meta["color"]+';color:#fff;border-radius:50%;width:18px;height:18px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700">✓</span>' if is_sel else ""
        with col:
            st.markdown(
                f'<div style="position:relative;background:{bg};border:2px solid {border};border-radius:14px;padding:16px;margin-bottom:8px;min-height:130px;box-shadow:{shadow};overflow:hidden">'
                f'{check}<div style="font-size:1.5rem;margin-bottom:6px">{meta["icon"]}</div>'
                f'<div style="font-weight:700;font-size:0.95rem;margin-bottom:3px">{mood_name}</div>'
                f'<div style="font-size:0.8rem;opacity:0.6;margin-bottom:8px">{meta["desc"]}</div>'
                f'<span style="font-size:0.7rem;font-weight:700;color:{meta["color"]};border:1px solid {meta["color"]};padding:2px 9px;border-radius:20px">{meta["tag"]}</span>'
                f'</div>',unsafe_allow_html=True)
            lbl = f"✓ Selected" if is_sel else f"Select {mood_name}"
            if st.button(lbl, key=f"mood_{mood_name}", use_container_width=True):
                st.session_state["mood"] = mood_name; st.rerun()

    st.markdown("---")
    amount = st.number_input("How much do you want to invest today? ($)", min_value=50.0, max_value=1_000_000.0, value=500.0, step=50.0, format="%.0f")
    generate = st.button("Build my investment plan", type="primary", use_container_width=True)
    mood = st.session_state.get("mood",None)
    if generate and not mood:
        st.warning("Please select a mood above first."); return
    if generate and mood and amount:
        profile = PROFILES[mood]; meta = MOOD_META[mood]
        st.markdown("---")
        st.subheader(f"{meta['icon']} Your {mood} plan — ${amount:,.0f}")
        m1,m2,m3 = st.columns(3)
        m1.metric("Expected return",profile["expected"]); m2.metric("Horizon",profile["horizon"]); m3.metric("Volatility",profile["volatility"])
        st.markdown("&nbsp;")
        cc, tc = st.columns([1,1.6])
        colors=["#1D9E75","#378ADD","#D85A30","#BA7517","#7F77DD","#888780"]
        with cc:
            fig=go.Figure(go.Pie(labels=[s["ticker"] for s in profile["stocks"]],values=[s["pct"] for s in profile["stocks"]],hole=0.52,marker_colors=colors,textinfo="label+percent",textfont_size=12))
            fig.update_layout(height=280,margin=dict(l=0,r=0,t=8,b=0),showlegend=False,paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig,use_container_width=True)
        with tc:
            risk_s={"Low":"rgba(29,158,117,0.15);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.3)","Mid":"rgba(186,117,23,0.15);color:#BA7517;border:0.5px solid rgba(186,117,23,0.3)","High":"rgba(216,90,48,0.15);color:#D85A30;border:0.5px solid rgba(216,90,48,0.3)"}
            for stock in profile["stocks"]:
                dollars=amount*stock["pct"]/100; rs=risk_s.get(stock["risk"],"")
                st.markdown(
                    f'<div style="background:rgba(128,128,128,0.06);border:0.5px solid rgba(128,128,128,0.13);border-radius:12px;padding:10px 14px;margin-bottom:8px">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'
                    f'<span style="font-weight:700">{stock["ticker"]}</span>'
                    f'<div style="display:flex;gap:8px;align-items:center"><span style="background:{rs};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:600">{stock["risk"]} risk</span>'
                    f'<span style="font-weight:700;color:{meta["color"]};font-size:1rem">${dollars:,.0f}</span>'
                    f'<span style="font-size:0.75rem;opacity:0.4">{stock["pct"]}%</span></div></div>'
                    f'<div style="font-size:0.78rem;opacity:0.6;line-height:1.45">{stock["rationale"]}</div></div>',
                    unsafe_allow_html=True)
        st.caption("⚠️ Not financial advice. Past performance does not guarantee future results.")
