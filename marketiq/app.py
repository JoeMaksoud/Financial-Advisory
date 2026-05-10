import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MarketIQ — AI Investment Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Hide Streamlit chrome via st.markdown (this part works fine) ──────────────
st.markdown("""
<style>
  #MainMenu, footer, header,
  [data-testid="stSidebar"],
  [data-testid="collapsedControl"],
  .stDeployButton { display:none !important; }
  .block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
  }
  [data-testid="stMain"] > div { padding-top: 0 !important; }

  /* shared component styles used by all pages */
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
</style>
""", unsafe_allow_html=True)


# ── Sticky nav via components.html (renders true HTML in an iframe-like block) -
def render_nav(active: str):
    pages = [
        ("dashboard",   "📊", "Dashboard"),
        ("news",        "📰", "News → Stocks"),
        ("plan",        "🎯", "My Plan"),
        ("projections", "📈", "Projections"),
    ]

    btns = ""
    for key, icon, label in pages:
        is_active = key == active
        active_style = (
            "background:rgba(29,158,117,0.12);color:#1D9E75;"
            "border:1px solid rgba(29,158,117,0.28);font-weight:600;"
        ) if is_active else (
            "background:transparent;color:#888;border:1px solid transparent;"
        )
        icon_bg = "background:rgba(29,158,117,0.15);" if is_active else "background:rgba(128,128,128,0.10);"
        dot = '<span style="width:5px;height:5px;border-radius:50%;background:#1D9E75;margin-left:4px;display:inline-block"></span>' if is_active else ""

        btns += f"""
        <a href="?page={key}" style="text-decoration:none">
          <div style="display:flex;align-items:center;gap:7px;padding:7px 13px;
               border-radius:10px;font-size:12px;cursor:pointer;
               transition:all 0.15s;white-space:nowrap;{active_style}"
               onmouseover="if(!this.classList.contains('act')){{this.style.background='rgba(128,128,128,0.10)';this.style.color='var(--color-text-primary)'}}"
               onmouseout="if(!this.classList.contains('act')){{this.style.background='transparent';this.style.color='#888'}}">
            <span style="width:26px;height:26px;border-radius:7px;display:flex;
                  align-items:center;justify-content:center;font-size:13px;{icon_bg}">{icon}</span>
            <span>{label}</span>
            {dot}
          </div>
        </a>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: transparent;
    overflow: hidden;
  }}
  .nav {{
    display: flex;
    align-items: center;
    height: 56px;
    padding: 0 24px;
    gap: 4px;
    background: transparent;
    border-bottom: 1px solid rgba(128,128,128,0.18);
  }}
  .brand {{
    display: flex; align-items: center; gap: 9px;
    margin-right: 18px; flex-shrink: 0;
    text-decoration: none;
  }}
  .brand-icon {{
    width: 32px; height: 32px; border-radius: 9px;
    background: linear-gradient(135deg,#1D9E75 0%,#378ADD 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
  }}
  .brand-name {{ font-size:14px;font-weight:600;color:#1D9E75;letter-spacing:-0.2px; }}
  .brand-sub  {{ font-size:10px;color:#888;letter-spacing:0.03em; }}
  .nav-items  {{ display:flex;align-items:center;gap:3px;flex:1; }}
  .nav-right  {{ display:flex;align-items:center;gap:10px;margin-left:auto; }}
  .live       {{ display:flex;align-items:center;gap:5px;font-size:11px;color:#888; }}
  .live-dot   {{ width:7px;height:7px;border-radius:50%;background:#1D9E75;
                  animation:pulse 1.8s infinite; }}
  @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.25}} }}
</style>
</head>
<body>
<div class="nav">
  <a class="brand" href="?page=dashboard">
    <div class="brand-icon">📈</div>
    <div>
      <div class="brand-name">MarketIQ</div>
      <div class="brand-sub">AI Investment Advisor</div>
    </div>
  </a>
  <div class="nav-items">{btns}</div>
  <div class="nav-right">
    <div class="live"><div class="live-dot"></div>Live prices</div>
  </div>
</div>
</body>
</html>"""

    # Render in a fixed-height iframe that sits at the very top
    components.html(html, height=58, scrolling=False)

    # Now use CSS to make that iframe sticky
    st.markdown("""
    <style>
      /* Target the iframe Streamlit wraps components.html in */
      [data-testid="stCustomComponentV1"] iframe,
      iframe[title="streamlit_components.v1.html"] {
        position: sticky !important;
        top: 0 !important;
        z-index: 9999 !important;
        display: block !important;
        width: 100% !important;
        border: none !important;
        background: var(--color-background-primary) !important;
        box-shadow: 0 1px 0 rgba(128,128,128,0.15) !important;
      }
      /* Also make the stCustomComponentV1 wrapper sticky */
      [data-testid="stCustomComponentV1"] {
        position: sticky !important;
        top: 0 !important;
        z-index: 9999 !important;
        background: var(--color-background-primary) !important;
        box-shadow: 0 1px 0 rgba(128,128,128,0.15) !important;
        margin-bottom: 0 !important;
      }
    </style>
    """, unsafe_allow_html=True)


# ── Route ─────────────────────────────────────────────────────────────────────
page = st.query_params.get("page", "dashboard")

render_nav(page)

if page == "dashboard":
    from pages.dashboard import show
    show()
elif page == "news":
    from pages.news_stocks import show
    show()
elif page == "plan":
    from pages.mood_allocator import show
    show()
elif page == "projections":
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
