import streamlit as st

st.set_page_config(
    page_title="MarketIQ — Your AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  /* ── Reset hardcoded backgrounds ── */
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  h1, h2, h3 { font-weight: 600; }

  /* ── Dynamic text: always readable in light & dark ── */
  :root {
    --text-primary:   inherit;
    --text-muted:     rgba(128,128,128,1);
    --border-color:   rgba(128,128,128,0.18);
    --card-bg:        rgba(128,128,128,0.06);
    --card-bg-hover:  rgba(128,128,128,0.10);
    --card-border:    rgba(128,128,128,0.15);
    --accent-green:   #1D9E75;
    --accent-red:     #D85A30;
    --accent-blue:    #378ADD;
    --accent-gold:    #BA7517;
  }

  /* ── Metric cards: transparent bg, dynamic text ── */
  .stMetric label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.6;
  }
  .stMetric [data-testid="metric-container"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 0.9rem 1.1rem;
    backdrop-filter: blur(4px);
    transition: box-shadow 0.2s;
  }
  .stMetric [data-testid="metric-container"]:hover {
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  }

  /* ── Badges ── */
  .badge-buy   { background:rgba(29,158,117,0.15); color:#1D9E75; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; border:1px solid rgba(29,158,117,0.3); }
  .badge-sell  { background:rgba(216,90,48,0.13);  color:#D85A30; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; border:1px solid rgba(216,90,48,0.3); }
  .badge-hold  { background:rgba(128,128,128,0.12);color:inherit;  padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; border:1px solid rgba(128,128,128,0.25); opacity:0.8; }
  .badge-watch { background:rgba(186,117,23,0.13); color:#BA7517; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; border:1px solid rgba(186,117,23,0.3); }

  /* ── News / rec cards: transparent, artistic border ── */
  .news-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(4px);
    transition: box-shadow 0.2s, transform 0.15s;
    position: relative;
    overflow: hidden;
  }
  .news-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-green), var(--accent-blue), var(--accent-gold));
    opacity: 0.5;
    border-radius: 16px 16px 0 0;
  }
  .news-card:hover {
    box-shadow: 0 6px 28px rgba(0,0,0,0.10);
    transform: translateY(-1px);
  }

  .rec-box {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    transition: box-shadow 0.2s;
  }
  .rec-box:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  }

  /* ── Tag pills ── */
  .tag-risk  { background:rgba(216,90,48,0.13);  color:#D85A30; padding:2px 9px; border-radius:20px; font-size:0.7rem; font-weight:700; border:1px solid rgba(216,90,48,0.25); }
  .tag-opp   { background:rgba(29,158,117,0.13); color:#1D9E75; padding:2px 9px; border-radius:20px; font-size:0.7rem; font-weight:700; border:1px solid rgba(29,158,117,0.25); }
  .tag-watch { background:rgba(186,117,23,0.13); color:#BA7517; padding:2px 9px; border-radius:20px; font-size:0.7rem; font-weight:700; border:1px solid rgba(186,117,23,0.25); }

  /* ── Stock rows: transparent, subtle separator ── */
  .stock-row-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 0;
    border-bottom: 1px solid var(--border-color);
  }
  .stock-row-item:last-child { border-bottom: none; }

  /* ── Section divider ── */
  .section-div { border-top: 1px solid var(--border-color); margin: 1.5rem 0; }

  /* ── Sentiment bar track ── */
  .sent-track {
    background: rgba(128,128,128,0.15);
    border-radius: 6px;
    height: 7px;
    overflow: hidden;
  }
  .sent-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.6s ease;
  }

  /* ── Hide default sidebar nav ── */
  div[data-testid="stSidebarNav"] { display: none; }

  /* ── Sidebar polish ── */
  [data-testid="stSidebar"] {
    border-right: 1px solid var(--border-color);
  }

  /* ── Button style ── */
  .stButton > button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: box-shadow 0.15s, transform 0.1s !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12) !important;
  }
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
