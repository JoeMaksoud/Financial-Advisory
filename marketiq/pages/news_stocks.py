import streamlit as st
from data.stock_data import NEWS_EVENTS


def _type_badge(t: str) -> str:
    styles = {
        "Risk":        "background:#fee2e2;color:#991b1b",
        "Opportunity": "background:#d1fae5;color:#065f46",
        "Watch":       "background:#fef3c7;color:#92400e",
    }
    style = styles.get(t, "background:#f3f4f6;color:#374151")
    return f'<span style="{style};padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:600">{t}</span>'


def _action_badge(action: str) -> tuple[str, str]:
    """Returns (bg_color, text_color)"""
    if action in ("Buy", "Strong Buy", "Add", "Add more", "Keep DCA"):
        return "#1D9E75", "#fff"
    if action in ("Avoid", "Sell"):
        return "#D85A30", "#fff"
    return "#888780", "#fff"


def show():
    st.title("📰 News → Stock Recommendations")
    st.caption(
        "Every global event translated into specific buy / hold / avoid actions for your portfolio."
    )

    # ── summary bar ──────────────────────────────────────────────────────────
    risks = sum(1 for e in NEWS_EVENTS if e["type"] == "Risk")
    opps  = sum(1 for e in NEWS_EVENTS if e["type"] == "Opportunity")
    watch = sum(1 for e in NEWS_EVENTS if e["type"] == "Watch")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Events tracked", len(NEWS_EVENTS))
    c2.metric("Risk events", risks, delta=None)
    c3.metric("Opportunities", opps)
    c4.metric("Watching", watch)

    st.markdown("---")

    # ── filter ───────────────────────────────────────────────────────────────
    filter_type = st.segmented_control(
        "Filter by type",
        options=["All", "Risk", "Opportunity", "Watch"],
        default="All",
        label_visibility="collapsed",
    )

    events = NEWS_EVENTS if filter_type == "All" else [e for e in NEWS_EVENTS if e["type"] == filter_type]

    # ── event cards ──────────────────────────────────────────────────────────
    for event in events:
        with st.container():
            type_html = _type_badge(event["type"])
            st.markdown(
                f"""<div class="news-card">
                  <div style="margin-bottom:8px">{type_html}
                    &nbsp;<span style="font-size:0.72rem;color:#888;font-weight:500">{event['category'].upper()}</span>
                  </div>
                  <div style="font-weight:600;font-size:1rem;margin-bottom:6px">{event['headline']}</div>
                  <div style="font-size:0.83rem;color:#555;line-height:1.55">{event['logic']}</div>
                </div>""",
                unsafe_allow_html=True,
            )

            st.markdown("**What to do with your money:**")
            cols = st.columns(len(event["actions"]))
            for col, action in zip(cols, event["actions"]):
                bg, fg = _action_badge(action["action"])
                risk_colors = {"low": ("#d1fae5", "#065f46"), "mid": ("#fef3c7", "#92400e"), "high": ("#fee2e2", "#991b1b")}
                rbg, rfg = risk_colors.get(action["risk"], ("#f3f4f6", "#374151"))
                with col:
                    st.markdown(
                        f"""<div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:12px;height:100%">
                          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                            <span style="font-weight:700;font-size:0.95rem">{action['ticker']}</span>
                            <span style="background:{bg};color:{fg};padding:2px 9px;border-radius:20px;font-size:0.68rem;font-weight:600">{action['action']}</span>
                          </div>
                          <div style="font-size:0.78rem;color:#555;line-height:1.5;margin-bottom:8px">{action['reason']}</div>
                          <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#888">
                            <span style="background:{rbg};color:{rfg};padding:1px 7px;border-radius:10px;font-weight:500">{action['risk'].capitalize()} risk</span>
                            <span>{action['horizon']}</span>
                          </div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

            st.markdown("&nbsp;")
