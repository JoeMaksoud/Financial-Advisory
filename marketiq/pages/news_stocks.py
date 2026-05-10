import streamlit as st
from data.stock_data import NEWS_EVENTS


def _type_badge(t):
    styles = {
        "Risk":        "background:rgba(216,90,48,0.13);color:#D85A30;border:1px solid rgba(216,90,48,0.3)",
        "Opportunity": "background:rgba(29,158,117,0.13);color:#1D9E75;border:1px solid rgba(29,158,117,0.3)",
        "Watch":       "background:rgba(186,117,23,0.13);color:#BA7517;border:1px solid rgba(186,117,23,0.3)",
    }
    style = styles.get(t, "background:rgba(128,128,128,0.1);color:inherit")
    return f'<span style="{style};padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:700">{t}</span>'


def _action_pill(action):
    if action in ("Buy", "Strong Buy", "Add", "Add more", "Keep DCA"):
        return "background:rgba(29,158,117,0.15);color:#1D9E75;border:1px solid rgba(29,158,117,0.3)"
    if action in ("Avoid", "Sell"):
        return "background:rgba(216,90,48,0.13);color:#D85A30;border:1px solid rgba(216,90,48,0.3)"
    return "background:rgba(128,128,128,0.1);opacity:0.7;border:1px solid rgba(128,128,128,0.25)"


def _risk_pill(risk):
    palettes = {
        "low":  "background:rgba(29,158,117,0.12);color:#1D9E75;border:1px solid rgba(29,158,117,0.25)",
        "mid":  "background:rgba(186,117,23,0.12);color:#BA7517;border:1px solid rgba(186,117,23,0.25)",
        "high": "background:rgba(216,90,48,0.12);color:#D85A30;border:1px solid rgba(216,90,48,0.25)",
    }
    label = {"low": "Low risk", "mid": "Mid risk", "high": "High risk"}.get(risk, risk)
    style = palettes.get(risk, "")
    return f'<span style="{style};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:600">{label}</span>'


def _accent_for_type(t):
    return {
        "Risk":        "linear-gradient(90deg,#D85A30,#BA7517)",
        "Opportunity": "linear-gradient(90deg,#1D9E75,#378ADD)",
        "Watch":       "linear-gradient(90deg,#BA7517,#888780)",
    }.get(t, "rgba(128,128,128,0.4)")


def show():
    st.title("📰 News → Stock Recommendations")
    st.caption("Every global event translated into specific buy / hold / avoid actions for your portfolio.")

    # summary
    risks = sum(1 for e in NEWS_EVENTS if e["type"] == "Risk")
    opps  = sum(1 for e in NEWS_EVENTS if e["type"] == "Opportunity")
    watch = sum(1 for e in NEWS_EVENTS if e["type"] == "Watch")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Events tracked", len(NEWS_EVENTS))
    c2.metric("Risk events", risks)
    c3.metric("Opportunities", opps)
    c4.metric("Watching", watch)

    st.markdown("---")

    filter_type = st.segmented_control(
        "Filter", options=["All", "Risk", "Opportunity", "Watch"],
        default="All", label_visibility="collapsed",
    )
    events = NEWS_EVENTS if filter_type == "All" else [e for e in NEWS_EVENTS if e["type"] == filter_type]

    for event in events:
        accent = _accent_for_type(event["type"])

        # card shell
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.05);border:1px solid rgba(128,128,128,0.14);'
            f'border-radius:16px;padding:1rem 1.25rem 0.5rem;margin-bottom:1rem;'
            f'position:relative;overflow:hidden;box-shadow:0 2px 14px rgba(0,0,0,0.05);">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;'
            f'background:{accent};border-radius:16px 16px 0 0;opacity:0.7;"></div>'
            f'{_type_badge(event["type"])}'
            f'&nbsp;<span style="font-size:0.72rem;opacity:0.45;font-weight:500;letter-spacing:0.05em">'
            f'{event["category"].upper()}</span>'
            f'<div style="font-weight:600;font-size:1rem;margin:6px 0 4px">{event["headline"]}</div>'
            f'<div style="font-size:0.83rem;opacity:0.65;line-height:1.55;margin-bottom:0.75rem">{event["logic"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p style="font-size:0.8rem;font-weight:600;opacity:0.5;text-transform:uppercase;'
            'letter-spacing:0.06em;margin:0 0 8px">What to do with your money</p>',
            unsafe_allow_html=True,
        )

        cols = st.columns(len(event["actions"]))
        for col, action in zip(cols, event["actions"]):
            ap = _action_pill(action["action"])
            rp = _risk_pill(action["risk"])
            with col:
                st.markdown(
                    f'<div style="background:rgba(128,128,128,0.06);border:1px solid rgba(128,128,128,0.13);'
                    f'border-radius:14px;padding:12px;height:100%;transition:box-shadow 0.2s;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
                    f'  <span style="font-weight:700;font-size:0.95rem">{action["ticker"]}</span>'
                    f'  <span style="{ap};padding:2px 9px;border-radius:20px;font-size:0.68rem;font-weight:700">'
                    f'    {action["action"]}</span>'
                    f'</div>'
                    f'<div style="font-size:0.78rem;opacity:0.65;line-height:1.5;margin-bottom:8px">{action["reason"]}</div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'  {rp}'
                    f'  <span style="font-size:0.7rem;opacity:0.45">{action["horizon"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("&nbsp;")
