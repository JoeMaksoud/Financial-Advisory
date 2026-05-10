import streamlit as st

st.set_page_config(
    page_title="MarketIQ — AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header, [data-testid="stSidebar"],
  [data-testid="collapsedControl"], .stDeployButton { display: none !important; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  [data-testid="stAppViewContainer"] { padding: 0 !important; }

  /* ── Sticky nav bar ── */
  .miq-nav {
    position: sticky; top: 0; z-index: 1000;
    background: var(--color-background-primary);
    border-bottom: 0.5px solid var(--color-border-tertiary);
    display: flex; align-items: center; gap: 0;
    height: 52px; padding: 0 24px;
    backdrop-filter: blur(8px);
  }
  .miq-brand {
    font-size: 14px; font-weight: 500;
    color: var(--color-text-primary);
    display: flex; align-items: center; gap: 8px;
    margin-right: 28px; flex-shrink: 0; text-decoration: none;
  }
  .miq-brand-dot {
    width: 9px; height: 9px; border-radius: 50%; background: #1D9E75;
  }
  .miq-nav-items { display: flex; align-items: center; gap: 0; flex: 1; }
  .miq-nav-item {
    padding: 0 14px; height: 52px; display: flex; align-items: center;
    font-size: 12px; font-weight: 500;
    color: var(--color-text-secondary);
    text-decoration: none; border-bottom: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s; white-space: nowrap;
    cursor: pointer;
  }
  .miq-nav-item:hover { color: var(--color-text-primary); }
  .miq-nav-item.active { color: #1D9E75; border-bottom: 2px solid #1D9E75; }
  .miq-nav-right {
    display: flex; align-items: center; gap: 10px; margin-left: auto;
  }
  .miq-live {
    display: flex; align-items: center; gap: 5px;
    font-size: 11px; color: var(--color-text-secondary);
  }
  .miq-live-dot {
    width: 6px; height: 6px; border-radius: 50%; background: #1D9E75;
    animation: pulse 1.8s infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
  .miq-refresh-btn {
    font-size: 11px; padding: 4px 12px;
    border-radius: 20px;
    border: 0.5px solid var(--color-border-secondary);
    color: var(--color-text-secondary);
    background: transparent; cursor: pointer;
    transition: background 0.15s;
  }
  .miq-refresh-btn:hover { background: var(--color-background-secondary); }

  /* ── Section anchors ── */
  .miq-section { padding: 28px 32px; }
  .miq-section-label {
    font-size: 10px; font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.07em; color: var(--color-text-secondary);
    opacity: 0.5; margin-bottom: 14px;
  }
  .miq-section-divider {
    height: 0.5px; background: var(--color-border-tertiary); margin: 0 32px;
  }

  /* ── Metric cards ── */
  .stMetric label {
    font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.06em; opacity: 0.55;
  }
  .stMetric [data-testid="metric-container"] {
    background: rgba(128,128,128,0.06) !important;
    border: 0.5px solid rgba(128,128,128,0.15);
    border-radius: 12px; padding: 0.85rem 1rem;
    transition: box-shadow 0.2s;
  }
  .stMetric [data-testid="metric-container"]:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
  }

  /* ── Badges ── */
  .badge-buy   { background:rgba(29,158,117,0.15);color:#1D9E75;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(29,158,117,0.3); }
  .badge-sell  { background:rgba(216,90,48,0.13);color:#D85A30;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(216,90,48,0.3); }
  .badge-hold  { background:rgba(128,128,128,0.10);padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(128,128,128,0.25);opacity:0.8; }
  .badge-watch { background:rgba(186,117,23,0.13);color:#BA7517;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;border:0.5px solid rgba(186,117,23,0.3); }

  /* ── Stock rows ── */
  .stock-row-item {
    display:flex;justify-content:space-between;align-items:center;
    padding:9px 0;border-bottom:0.5px solid rgba(128,128,128,0.12);
  }
  .stock-row-item:last-child { border-bottom:none; }

  /* ── Cards ── */
  .miq-card {
    background:rgba(128,128,128,0.06);border:0.5px solid rgba(128,128,128,0.15);
    border-radius:16px;padding:1rem 1.25rem;margin-bottom:0.75rem;
    position:relative;overflow:hidden;
  }
  .miq-card::before {
    content:"";position:absolute;top:0;left:0;right:0;height:2px;
    border-radius:16px 16px 0 0;opacity:0.7;
  }
  .miq-card:hover { box-shadow:0 4px 20px rgba(0,0,0,0.07); }

  /* ── News cards ── */
  .news-card {
    background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.14);
    border-radius:16px;padding:1rem 1.25rem 0.5rem;margin-bottom:1rem;
    position:relative;overflow:hidden;
  }

  /* ── Mood cards ── */
  .mood-card {
    background:rgba(128,128,128,0.05);border:1.5px solid rgba(128,128,128,0.15);
    border-radius:14px;padding:16px;margin-bottom:8px;
    position:relative;overflow:hidden;min-height:130px;
    transition:box-shadow 0.2s;
  }

  /* ── Sentiment bars ── */
  .sent-track { background:rgba(128,128,128,0.15);border-radius:6px;height:7px;overflow:hidden; }
  .sent-fill  { height:100%;border-radius:6px; }

  /* ── Buttons ── */
  .stButton > button {
    border-radius:10px !important; font-weight:500 !important;
    transition:box-shadow 0.15s, transform 0.1s !important;
  }
  .stButton > button:hover {
    transform:translateY(-1px) !important;
    box-shadow:0 4px 14px rgba(0,0,0,0.10) !important;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width:4px; height:4px; }
  ::-webkit-scrollbar-track { background:transparent; }
  ::-webkit-scrollbar-thumb { background:rgba(128,128,128,0.25);border-radius:4px; }
</style>

<div class="miq-nav">
  <a class="miq-brand" href="#overview">
    <div class="miq-brand-dot"></div>MarketIQ
  </a>
  <div class="miq-nav-items">
    <a class="miq-nav-item active" href="#overview">Overview</a>
    <a class="miq-nav-item" href="#signals">Signals</a>
    <a class="miq-nav-item" href="#news">News → Stocks</a>
    <a class="miq-nav-item" href="#plan">My Plan</a>
    <a class="miq-nav-item" href="#projections">Projections</a>
  </div>
  <div class="miq-nav-right">
    <div class="miq-live"><div class="miq-live-dot"></div>Live prices</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── inject section anchors + render each section ──────────────────────────────

def anchor(section_id: str):
    st.markdown(f'<div id="{section_id}" style="scroll-margin-top:60px"></div>',
                unsafe_allow_html=True)

def section_divider():
    st.markdown('<div class="miq-section-divider"></div>', unsafe_allow_html=True)

def section_label(text: str):
    st.markdown(f'<div class="miq-section-label">{text}</div>', unsafe_allow_html=True)

# ── Overview ──────────────────────────────────────────────────────────────────
anchor("overview")
with st.container():
    st.markdown('<div style="padding:28px 32px 0">', unsafe_allow_html=True)
    from pages.dashboard import show as show_dashboard
    show_dashboard()
    st.markdown('</div>', unsafe_allow_html=True)

section_divider()

# ── Signals (buy/sell lists are already in dashboard, skip duplicate) ─────────
# Signals section rendered as part of dashboard above.
# Add anchor for nav jump.
anchor("signals")

section_divider()

# ── News → Stocks ─────────────────────────────────────────────────────────────
anchor("news")
with st.container():
    st.markdown('<div style="padding:28px 32px 0">', unsafe_allow_html=True)
    from pages.news_stocks import show as show_news
    show_news()
    st.markdown('</div>', unsafe_allow_html=True)

section_divider()

# ── My Plan (Mood Allocator) ──────────────────────────────────────────────────
anchor("plan")
with st.container():
    st.markdown('<div style="padding:28px 32px 0">', unsafe_allow_html=True)
    from pages.mood_allocator import show as show_mood
    show_mood()
    st.markdown('</div>', unsafe_allow_html=True)

section_divider()

# ── Projections ───────────────────────────────────────────────────────────────
anchor("projections")
with st.container():
    st.markdown('<div style="padding:28px 32px 0">', unsafe_allow_html=True)
    from pages.projection import show as show_projection
    show_projection()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:24px 32px;border-top:0.5px solid rgba(128,128,128,0.15);
  display:flex;justify-content:space-between;align-items:center;
  font-size:11px;color:var(--color-text-secondary);opacity:0.5;margin-top:16px">
  <span>MarketIQ — AI Investment Advisor</span>
  <span>Not financial advice · Data via Yahoo Finance & public RSS · Prices refresh every 5 min</span>
</div>
""", unsafe_allow_html=True)
