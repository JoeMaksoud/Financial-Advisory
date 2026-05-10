import streamlit as st

st.set_page_config(
    page_title="MarketIQ — AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Hide Streamlit chrome ─────────────────────────────────────────────────────
st.markdown("""
<style>
  #MainMenu, footer, header,
  [data-testid="stSidebar"],
  [data-testid="collapsedControl"],
  .stDeployButton { display:none !important; }
  .block-container { padding-top:0 !important; padding-bottom:3rem !important; max-width:100% !important; }
  [data-testid="stMain"] > div { padding-top:0 !important; }

  /* ── Shared component styles ── */
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
  .mood-card { background:rgba(128,128,128,0.05);border:1.5px solid rgba(128,128,128,0.15);border-radius:14px;padding:16px;margin-bottom:8px;position:relative;overflow:hidden;min-height:130px;transition:box-shadow 0.2s; }
  .sent-track { background:rgba(128,128,128,0.15);border-radius:6px;height:7px;overflow:hidden; }
  .sent-fill  { height:100%;border-radius:6px; }
  .stButton > button { border-radius:10px !important;font-weight:500 !important;transition:box-shadow 0.15s,transform 0.1s !important; }
  .stButton > button:hover { transform:translateY(-1px) !important;box-shadow:0 4px 14px rgba(0,0,0,0.10) !important; }

  /* ── Nav bar shell — always visible, sticky ── */
  .miq-nav-shell {
    position: sticky; top: 0; z-index: 9999;
    background: var(--color-background-primary);
    border-bottom: 0.5px solid rgba(128,128,128,0.18);
    padding: 0 24px;
    display: flex; align-items: center;
    height: 56px; gap: 4px;
    backdrop-filter: blur(12px);
  }
  .miq-brand {
    display: flex; align-items: center; gap: 9px;
    margin-right: 18px; flex-shrink: 0;
  }
  .miq-brand-icon {
    width: 32px; height: 32px; border-radius: 9px;
    background: linear-gradient(135deg,#1D9E75,#378ADD);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
  }
  .miq-brand-name { font-size:14px;font-weight:600;color:#1D9E75;letter-spacing:-0.2px; }
  .miq-brand-sub  { font-size:10px;color:var(--color-text-secondary);opacity:0.55; }
  .miq-live {
    display:flex;align-items:center;gap:5px;font-size:11px;
    color:var(--color-text-secondary);opacity:0.6;margin-left:auto;
  }
  .miq-live-dot {
    width:6px;height:6px;border-radius:50%;background:#1D9E75;
    animation:miq-pulse 1.8s infinite;
  }
  @keyframes miq-pulse { 0%,100%{opacity:1} 50%{opacity:0.25} }

  /* ── Nav buttons rendered by Streamlit ── */
  div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0 !important;
  }

  /* Style nav buttons to look like proper nav items */
  .nav-btn > div > div > div > button {
    display: flex !important;
    align-items: center !important;
    gap: 7px !important;
    padding: 7px 13px !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    height: 36px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: var(--color-text-secondary) !important;
    white-space: nowrap !important;
    width: auto !important;
  }
  .nav-btn > div > div > div > button:hover {
    background: rgba(128,128,128,0.10) !important;
    border-color: rgba(128,128,128,0.18) !important;
    color: var(--color-text-primary) !important;
    transform: none !important;
    box-shadow: none !important;
  }
  .nav-btn-active > div > div > div > button {
    background: rgba(29,158,117,0.12) !important;
    border-color: rgba(29,158,117,0.28) !important;
    color: #1D9E75 !important;
    font-weight: 600 !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Session state routing ─────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

PAGES = [
    ("dashboard",   "📊", "Dashboard"),
    ("news",        "📰", "News → Stocks"),
    ("plan",        "🎯", "My Plan"),
    ("projections", "📈", "Projections"),
]

# ── Sticky nav bar ────────────────────────────────────────────────────────────
st.markdown("""
<div class="miq-nav-shell">
  <div class="miq-brand">
    <div class="miq-brand-icon">📈</div>
    <div>
      <div class="miq-brand-name">MarketIQ</div>
      <div class="miq-brand-sub">AI Investment Advisor</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Render nav buttons using real Streamlit buttons (they actually work)
# We overlay them on top of the nav shell using negative margin trick
st.markdown("""
<style>
  /* Pull the button row up into the nav shell */
  div[data-testid="stHorizontalBlock"]:first-of-type {
    position: sticky;
    top: 0;
    z-index: 10000;
    background: var(--color-background-primary);
    border-bottom: 0.5px solid rgba(128,128,128,0.18);
    padding: 10px 24px 10px 220px;
    margin-top: -56px;
    backdrop-filter: blur(12px);
    gap: 4px !important;
  }
  div[data-testid="stHorizontalBlock"]:first-of-type > div {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 0 !important;
  }
  div[data-testid="stHorizontalBlock"]:first-of-type button {
    border-radius: 10px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 6px 13px !important;
    height: 36px !important;
    white-space: nowrap !important;
    min-height: 0 !important;
    line-height: 1 !important;
    border: 1px solid rgba(128,128,128,0.18) !important;
    color: var(--color-text-secondary) !important;
    background: transparent !important;
    transform: none !important;
    box-shadow: none !important;
  }
  div[data-testid="stHorizontalBlock"]:first-of-type button:hover {
    background: rgba(128,128,128,0.10) !important;
    color: var(--color-text-primary) !important;
    transform: none !important;
    box-shadow: none !important;
  }
  /* Active page button — highlighted green */
  div[data-testid="stHorizontalBlock"]:first-of-type div:nth-child(ACTIVE_IDX) button {
    background: rgba(29,158,117,0.12) !important;
    border-color: rgba(29,158,117,0.30) !important;
    color: #1D9E75 !important;
    font-weight: 600 !important;
  }
  /* Live dot area */
  div[data-testid="stHorizontalBlock"]:first-of-type > div:last-child {
    margin-left: auto !important;
  }
</style>
""".replace("ACTIVE_IDX", str([p[0] for p in PAGES].index(st.session_state.page) + 1)),
unsafe_allow_html=True)

# Render actual clickable Streamlit buttons in a row
nav_cols = st.columns([1, 1, 1, 1, 2])  # 4 buttons + spacer for live dot
for i, (key, icon, label) in enumerate(PAGES):
    with nav_cols[i]:
        if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=False):
            st.session_state.page = key
            st.rerun()

with nav_cols[4]:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:5px;justify-content:flex-end;'
        'height:36px;font-size:11px;color:var(--color-text-secondary);opacity:0.6">'
        '<div style="width:6px;height:6px;border-radius:50%;background:#1D9E75;'
        'animation:miq-pulse 1.8s infinite"></div>Live prices</div>',
        unsafe_allow_html=True
    )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Route to page ─────────────────────────────────────────────────────────────
current = st.session_state.page

if current == "dashboard":
    from pages.dashboard import show
    show()
elif current == "news":
    from pages.news_stocks import show
    show()
elif current == "plan":
    from pages.mood_allocator import show
    show()
elif current == "projections":
    from pages.projection import show
    show()
else:
    from pages.dashboard import show
    show()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:32px;padding:20px 0 0;border-top:0.5px solid rgba(128,128,128,0.12);
  font-size:11px;color:var(--color-text-secondary);opacity:0.4;
  display:flex;justify-content:space-between">
  <span>MarketIQ — AI Investment Advisor</span>
  <span>Not financial advice · Prices refresh every 5 min · Data via Yahoo Finance</span>
</div>
""", unsafe_allow_html=True)
