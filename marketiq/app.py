import streamlit as st

st.set_page_config(
    page_title="MarketIQ — AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  h1, h2, h3 { font-weight: 600; }

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

  .stock-row-item { display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:0.5px solid rgba(128,128,128,0.12); }
  .stock-row-item:last-child { border-bottom:none; }

  .miq-card { background:rgba(128,128,128,0.06);border:0.5px solid rgba(128,128,128,0.15);border-radius:16px;padding:1rem 1.25rem;margin-bottom:0.75rem;position:relative;overflow:hidden;transition:box-shadow 0.2s; }
  .miq-card:hover { box-shadow:0 4px 20px rgba(0,0,0,0.07); }

  .news-card { background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.14);border-radius:16px;padding:1rem 1.25rem 0.5rem;margin-bottom:1rem;position:relative;overflow:hidden; }
  .news-card::before { content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent-green),var(--accent-blue),var(--accent-gold));opacity:0.5;border-radius:16px 16px 0 0; }
  .news-card:hover { box-shadow:0 6px 28px rgba(0,0,0,0.10);transform:translateY(-1px); }

  .rec-box { background:rgba(128,128,128,0.06);border:0.5px solid rgba(128,128,128,0.15);border-radius:14px;padding:0.9rem 1rem;margin-bottom:0.6rem;transition:box-shadow 0.2s; }
  .rec-box:hover { box-shadow:0 4px 20px rgba(0,0,0,0.08); }

  .mood-card { background:rgba(128,128,128,0.05);border:1.5px solid rgba(128,128,128,0.15);border-radius:14px;padding:16px;margin-bottom:8px;position:relative;overflow:hidden;min-height:130px;transition:box-shadow 0.2s; }

  .sent-track { background:rgba(128,128,128,0.15);border-radius:6px;height:7px;overflow:hidden; }
  .sent-fill  { height:100%;border-radius:6px; }

  .section-div { border-top:0.5px solid rgba(128,128,128,0.15);margin:1.5rem 0; }

  div[data-testid="stSidebarNav"] { display:none; }
  [data-testid="stSidebar"] { border-right:0.5px solid rgba(128,128,128,0.15); }

  .stButton > button { border-radius:10px !important;font-weight:500 !important;transition:box-shadow 0.15s,transform 0.1s !important; }
  .stButton > button:hover { transform:translateY(-1px) !important;box-shadow:0 4px 14px rgba(0,0,0,0.10) !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ─────────────────────────────────────────────────────────
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

# ── Route to page ──────────────────────────────────────────────────────────────
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
