import streamlit as st

st.set_page_config(
    page_title="MarketIQ — Your AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── shared CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-weight: 600; }
    .stMetric label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #888; }
    .stMetric [data-testid="metric-container"] { background: #f8f9fa; border-radius: 10px; padding: 0.8rem 1rem; }
    .badge-buy    { background:#d1fae5; color:#065f46; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:600; }
    .badge-sell   { background:#fee2e2; color:#991b1b; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:600; }
    .badge-hold   { background:#f3f4f6; color:#374151; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:600; }
    .badge-watch  { background:#fef3c7; color:#92400e; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:600; }
    .news-card    { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:1rem 1.25rem; margin-bottom:1rem; }
    .tag-risk     { background:#fee2e2; color:#991b1b; padding:2px 9px; border-radius:20px; font-size:0.7rem; font-weight:600; }
    .tag-opp      { background:#d1fae5; color:#065f46; padding:2px 9px; border-radius:20px; font-size:0.7rem; font-weight:600; }
    .tag-watch    { background:#fef3c7; color:#92400e; padding:2px 9px; border-radius:20px; font-size:0.7rem; font-weight:600; }
    .rec-box      { background:#f9fafb; border-radius:10px; padding:0.85rem 1rem; margin-bottom:0.6rem; }
    .section-div  { border-top:1px solid #e5e7eb; margin:1.5rem 0; }
    div[data-testid="stSidebarNav"] { display:none; }
</style>
""", unsafe_allow_html=True)

# ── sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📈 MarketIQ")
    st.markdown("Your AI Investment Advisor")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "📰 News → Stocks", "🎯 Mood Allocator", "📊 Projection Calculator"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Data uses historical averages & AI analysis. Not financial advice.")

# ── route to page ─────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    from pages import dashboard
    dashboard.show()
elif page == "📰 News → Stocks":
    from pages import news_stocks
    news_stocks.show()
elif page == "🎯 Mood Allocator":
    from pages import mood_allocator
    mood_allocator.show()
elif page == "📊 Projection Calculator":
    from pages import projection
    projection.show()
