import streamlit as st

st.set_page_config(
    page_title="MarketIQ — AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── shared nav CSS + sticky bar ───────────────────────────────────────────────
NAV_CSS = """
<style>
  #MainMenu, footer, header,
  [data-testid="stSidebar"],
  [data-testid="collapsedControl"],
  .stDeployButton { display:none !important; }

  .block-container { padding-top:0 !important; padding-bottom:3rem !important; max-width:100% !important; }
  [data-testid="stAppViewContainer"] { padding-top:0 !important; }
  [data-testid="stMain"] > div:first-child { padding-top:0 !important; }

  /* ── Sticky nav wrapper ── */
  .miq-nav-wrap {
    position: sticky; top: 0; z-index: 9999;
    background: var(--color-background-primary);
    border-bottom: 0.5px solid var(--color-border-tertiary);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }
  .miq-nav {
    display: flex; align-items: center;
    height: 56px; padding: 0 28px; gap: 6px;
    max-width: 100%;
  }

  /* ── Brand ── */
  .miq-brand {
    display: flex; align-items: center; gap: 8px;
    margin-right: 20px; flex-shrink: 0;
    text-decoration: none;
  }
  .miq-brand-icon {
    width: 30px; height: 30px; border-radius: 8px;
    background: linear-gradient(135deg,#1D9E75,#378ADD);
    display: flex; align-items: center; justify-content: center;
    font-size: 15px;
  }
  .miq-brand-text {
    font-size: 14px; font-weight: 600;
    color: var(--color-text-primary); letter-spacing: -0.2px;
  }
  .miq-brand-sub {
    font-size: 10px; color: var(--color-text-secondary);
    opacity: 0.55; letter-spacing: 0.02em;
  }

  /* ── Nav buttons ── */
  .miq-nav-items { display:flex; align-items:center; gap:4px; flex:1; }

  .miq-btn {
    display: flex; align-items: center; gap: 7px;
    padding: 7px 14px; border-radius: 10px;
    font-size: 12px; font-weight: 500;
    color: var(--color-text-secondary);
    background: transparent;
    border: 0.5px solid transparent;
    cursor: pointer; text-decoration: none;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
    white-space: nowrap; position: relative;
  }
  .miq-btn:hover {
    background: var(--color-background-secondary);
    color: var(--color-text-primary);
    border-color: var(--color-border-tertiary);
  }
  .miq-btn.active {
    background: rgba(29,158,117,0.10);
    color: #1D9E75;
    border-color: rgba(29,158,117,0.25);
    font-weight: 600;
  }
  .miq-btn .btn-icon {
    width: 24px; height: 24px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; flex-shrink: 0;
    background: rgba(128,128,128,0.08);
    transition: background 0.15s;
  }
  .miq-btn.active .btn-icon {
    background: rgba(29,158,117,0.15);
  }
  .miq-btn:hover .btn-icon {
    background: rgba(128,128,128,0.14);
  }
  .miq-btn .btn-label { line-height: 1; }
  .miq-btn .btn-dot {
    width: 4px; height: 4px; border-radius: 50%;
    background: #1D9E75; margin-left: 2px;
    display: none;
  }
  .miq-btn.active .btn-dot { display: block; }

  /* ── Right side of nav ── */
  .miq-nav-right {
    display: flex; align-items: center; gap: 12px;
    margin-left: auto; flex-shrink: 0;
  }
  .miq-live {
    display: flex; align-items: center; gap: 5px;
    font-size: 11px; color: var(--color-text-secondary);
    opacity: 0.6;
  }
  .miq-live-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #1D9E75; animation: miq-pulse 1.8s infinite;
  }
  @keyframes miq-pulse { 0%,100%{opacity:1} 50%{opacity:0.25} }

  /* ── Page content padding ── */
  .miq-page { padding: 32px 40px; }

  /* ── Common component styles ── */
  .stMetric label { font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;opacity:0.55; }
  .stMetric [data-testid="metric-container"] {
    background:rgba(128,128,128,0.06) !important;
    border:0.5px solid rgba(128,128,128,0.15);
    border-radius:12px; padding:0.85rem 1rem;
    transition:box-shadow 0.2s;
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
</style>
"""


def render_nav(active: str):
    pages = [
        ("dashboard",  "📊", "Dashboard"),
        ("news",       "📰", "News → Stocks"),
        ("plan",       "🎯", "My Plan"),
        ("projections","📈", "Projections"),
    ]
    btns_html = ""
    for key, icon, label in pages:
        cls = "miq-btn active" if key == active else "miq-btn"
        btns_html += (
            f'<a class="{cls}" href="?page={key}" style="text-decoration:none">'
            f'<span class="btn-icon">{icon}</span>'
            f'<span class="btn-label">{label}</span>'
            f'<span class="btn-dot"></span>'
            f'</a>'
        )
    st.markdown(f"""
    {NAV_CSS}
    <div class="miq-nav-wrap">
      <div class="miq-nav">
        <a class="miq-brand" href="?page=dashboard" style="text-decoration:none">
          <div class="miq-brand-icon">📈</div>
          <div>
            <div class="miq-brand-text">MarketIQ</div>
            <div class="miq-brand-sub">AI Investment Advisor</div>
          </div>
        </a>
        <div class="miq-nav-items">{btns_html}</div>
        <div class="miq-nav-right">
          <div class="miq-live"><div class="miq-live-dot"></div>Live prices</div>
        </div>
      </div>
    </div>
    <div class="miq-page">
    """, unsafe_allow_html=True)


def close_page():
    st.markdown("""
    <div style="padding:24px 0 0;border-top:0.5px solid rgba(128,128,128,0.12);
      margin-top:32px;font-size:11px;color:var(--color-text-secondary);opacity:0.4;
      display:flex;justify-content:space-between">
      <span>MarketIQ — AI Investment Advisor</span>
      <span>Not financial advice · Prices refresh every 5 min · Data via Yahoo Finance</span>
    </div>
    </div>
    """, unsafe_allow_html=True)


# ── Route ─────────────────────────────────────────────────────────────────────
params = st.query_params
page   = params.get("page", "dashboard")

if page == "dashboard":
    render_nav("dashboard")
    from pages.dashboard import show
    show()
    close_page()

elif page == "news":
    render_nav("news")
    from pages.news_stocks import show
    show()
    close_page()

elif page == "plan":
    render_nav("plan")
    from pages.mood_allocator import show
    show()
    close_page()

elif page == "projections":
    render_nav("projections")
    from pages.projection import show
    show()
    close_page()

else:
    render_nav("dashboard")
    from pages.dashboard import show
    show()
    close_page()
