import streamlit as st

st.set_page_config(
    page_title="MarketIQ — AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .block-container { padding-top:1.5rem; padding-bottom:2rem; }
  h1,h2,h3 { font-weight:600; }

  .stMetric label { font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;opacity:0.55; }
  .stMetric [data-testid="metric-container"] {
    background:rgba(128,128,128,0.06) !important;
    border:0.5px solid rgba(128,128,128,0.15);
    border-radius:12px; padding:0.85rem 1rem; transition:box-shadow 0.2s;
  }
  .stMetric [data-testid="metric-container"]:hover { box-shadow:0 4px 20px rgba(0,0,0,0.07); }

  .badge-buy   { background:rgba(29,158,117,0.15);color:#1D9E75;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(29,158,117,0.3); }
  .badge-sell  { background:rgba(216,90,48,0.13);color:#D85A30;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(216,90,48,0.3); }
  .badge-hold  { background:rgba(128,128,128,0.10);padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(128,128,128,0.25);opacity:0.8; }
  .badge-watch { background:rgba(186,117,23,0.13);color:#BA7517;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(186,117,23,0.3); }

  .sent-track { background:rgba(128,128,128,0.15);border-radius:6px;height:7px;overflow:hidden; }
  .sent-fill  { height:100%;border-radius:6px; }

  div[data-testid="stSidebarNav"] { display:none; }
  [data-testid="stSidebar"] { border-right:0.5px solid rgba(128,128,128,0.15); }

  .stButton > button { border-radius:10px !important;font-weight:500 !important;transition:box-shadow 0.15s,transform 0.1s !important; }
  .stButton > button:hover { transform:translateY(-1px) !important;box-shadow:0 4px 14px rgba(0,0,0,0.10) !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📈 MarketIQ")
    st.markdown("AI Investment Advisor")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "📰 News → Stocks",
            "🎯 My Plan",
            "📊 Projections",
            "🧠 Smart Money",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Recommendations based on fundamentals, macro trends, and global market analysis. Not financial advice.")

if page == "🏠 Dashboard":
    from pages.dashboard import show
elif page == "📰 News → Stocks":
    from pages.news_stocks import show
elif page == "🎯 My Plan":
    from pages.mood_allocator import show
elif page == "📊 Projections":
    from pages.projection import show
elif page == "🧠 Smart Money":
    from pages.smart_money import show

show()
