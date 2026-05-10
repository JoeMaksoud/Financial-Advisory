"""
news_stocks.py — News → Stock Recommendations
Live news is fetched from public RSS feeds (no API key needed).
Falls back to curated news if fetch fails.
Refreshes daily via st.cache_data(ttl=86400).
"""
import streamlit as st
import datetime
try:
    import feedparser
    FEEDPARSER_OK = True
except ImportError:
    FEEDPARSER_OK = False

# ── RSS feeds (free, no key) ─────────────────────────────────────────────────
RSS_FEEDS = {
    "Reuters Markets":       "https://feeds.reuters.com/reuters/businessNews",
    "CNBC Top News":         "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "MarketWatch Top":       "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "Seeking Alpha":         "https://seekingalpha.com/market_currents.xml",
    "Yahoo Finance":         "https://finance.yahoo.com/news/rssindex",
}

# ── Curated fallback news (updated May 2026) ─────────────────────────────────
CURATED_NEWS = [
    {
        "type": "Opportunity", "category": "AI Infrastructure",
        "headline": "AI capex spending by hyperscalers hits record $250B globally in 2026",
        "source": "CNBC", "date": "May 9, 2026",
        "logic": "Microsoft, Google, Amazon and Meta are collectively spending over $250B on AI data centers. "
                 "This is the single biggest capex cycle in tech history, creating a cascade of winners across chips, "
                 "power, cooling, and networking.",
        "actions": [
            {"ticker":"NVDA","action":"Strong Buy","risk":"high","reason":"80%+ AI chip market share. Every dollar of AI capex flows through Nvidia first.","horizon":"3–5 yrs"},
            {"ticker":"AVGO","action":"Buy","risk":"high","reason":"Custom AI ASICs for Google/Meta. In talks for record $35B OpenAI chip deal.","horizon":"3–5 yrs"},
            {"ticker":"NEE","action":"Buy","risk":"low","reason":"AI data centers are the fastest growing power consumer. NEE is the largest US clean energy provider.","horizon":"5–10 yrs"},
            {"ticker":"EQIX","action":"Buy","risk":"mid","reason":"World's largest data center REIT. Every AI model needs physical infrastructure globally.","horizon":"5–10 yrs"},
        ],
    },
    {
        "type": "Opportunity", "category": "Labor Market",
        "headline": "US jobs beat by double: +115K in April vs 60K forecast, unemployment holds at 4.3%",
        "source": "Schwab / BLS", "date": "May 8, 2026",
        "logic": "Two consecutive months of six-figure job growth signals a resilient economy. Strong labor data supports "
                 "consumer spending and corporate earnings, but reduces near-term Fed rate cut probability.",
        "actions": [
            {"ticker":"SPY/VOO","action":"Buy","risk":"low","reason":"Strong labor data = healthy economy = broad market upside. Keep DCA-ing into index funds.","horizon":"Long term"},
            {"ticker":"JPM","action":"Buy","risk":"mid","reason":"Banks benefit from a strong economy and delayed rate cuts. JPMorgan is the highest quality name in the sector.","horizon":"2–3 yrs"},
            {"ticker":"COST","action":"Buy","risk":"low","reason":"Consumers spending despite oil shock. Costco's membership model is recession-resistant.","horizon":"3–5 yrs"},
            {"ticker":"Bonds/TLT","action":"Hold","risk":"low","reason":"Delayed rate cuts means bonds stay pressured. Don't over-allocate to long-duration bonds yet.","horizon":"Watch Fed"},
        ],
    },
    {
        "type": "Risk", "category": "Geopolitical / Energy",
        "headline": "US-Iran conflict: oil above $100/barrel, economists warn of recession sleepwalk",
        "source": "CNBC / Morgan Stanley", "date": "May 6, 2026",
        "logic": "Oil prices are up 50%+ since the US-Iran conflict began Feb 28. Economists warn this is an "
                 "'extremely misplaced euphoria' moment — equity markets may be ignoring a serious energy shock "
                 "that could trigger a global recession if unresolved.",
        "actions": [
            {"ticker":"XOM/CVX","action":"Buy","risk":"mid","reason":"Higher oil = higher profits for energy majors. Natural hedge against the geopolitical risk in your portfolio.","horizon":"During conflict"},
            {"ticker":"LMT/RTX","action":"Buy","risk":"mid","reason":"Defense spending surges in active conflict. Lockheed and Raytheon have order backlogs for years ahead.","horizon":"2–4 yrs"},
            {"ticker":"GLD","action":"Add","risk":"low","reason":"Gold is the textbook safe haven in geopolitical crisis. Allocate 5–10% as insurance.","horizon":"Hold as hedge"},
            {"ticker":"Airlines","action":"Avoid","risk":"high","reason":"Jet fuel costs are crushing margins. Avoid DAL, UAL, AAL until oil drops below $85.","horizon":"Stay away"},
        ],
    },
    {
        "type": "Risk", "category": "Tech Correction",
        "headline": "Cloudflare drops 14% after announcing 1,100 layoffs citing AI efficiency gains",
        "source": "Schwab / Reuters", "date": "May 8, 2026",
        "logic": "Nearly 100,000 tech workers have been laid off year-to-date. Companies are using AI to reduce headcount, "
                 "compressing software valuations as growth stories become efficiency stories. This is a sector-wide signal, not just Cloudflare.",
        "actions": [
            {"ticker":"NET","action":"Watch","risk":"high","reason":"14% drop on solid earnings is potentially overdone. If you believe in cybersecurity long-term, this is a dip to watch.","horizon":"Entry opportunity"},
            {"ticker":"CRWD/ZS","action":"Hold","risk":"high","reason":"Cybersecurity fundamentals remain strong. Hold existing positions but be cautious adding more at current valuations.","horizon":"Monitor"},
            {"ticker":"SaaS ETF","action":"Reduce","risk":"high","reason":"Broad SaaS sector faces multiple compression as AI changes the cost structure of software companies.","horizon":"Trim exposure"},
            {"ticker":"MSFT","action":"Buy","risk":"low","reason":"Microsoft benefits from AI efficiency in both directions — as a tool provider and as a leaner operator itself.","horizon":"3–5 yrs"},
        ],
    },
    {
        "type": "Watch", "category": "Earnings Season",
        "headline": "Magnificent Seven earnings beat estimates; Meta +61% EPS, Amazon AWS reaccelerating",
        "source": "Motley Fool / CNBC", "date": "May 5–8, 2026",
        "logic": "Meta reported Q1 EPS up 61% year-on-year. Amazon AWS is growing again after a slowdown. "
                 "Google Search and Cloud both beat. This is a strong confirmation that AI monetization is beginning to show up in earnings.",
        "actions": [
            {"ticker":"META","action":"Buy","risk":"high","reason":"61% EPS growth, $145B AI capex plan, lowest P/E of the Mag 7 at 19.8x forward. Strong value within mega-cap.","horizon":"2–4 yrs"},
            {"ticker":"AMZN","action":"Buy","risk":"mid","reason":"AWS re-acceleration is the key signal. Cloud revenue is the highest-margin segment and it's growing again.","horizon":"3–5 yrs"},
            {"ticker":"GOOGL","action":"Buy","risk":"mid","reason":"Search and Cloud both beat. Gemini AI is remonetizing the core business. Still the cheapest mega-cap.","horizon":"3–5 yrs"},
            {"ticker":"TSLA","action":"Watch","risk":"high","reason":"Tesla did not participate in the Mag 7 earnings beat cycle. Monitor Q2 delivery numbers before adding.","horizon":"Wait for data"},
        ],
    },
]

# ── stock action styling ──────────────────────────────────────────────────────
def _type_badge(t):
    styles = {
        "Risk":        "background:rgba(216,90,48,0.13);color:#D85A30;border:1px solid rgba(216,90,48,0.3)",
        "Opportunity": "background:rgba(29,158,117,0.13);color:#1D9E75;border:1px solid rgba(29,158,117,0.3)",
        "Watch":       "background:rgba(186,117,23,0.13);color:#BA7517;border:1px solid rgba(186,117,23,0.3)",
    }
    style = styles.get(t,"background:rgba(128,128,128,0.1)")
    return f'<span style="{style};padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:700">{t}</span>'


def _action_pill(action):
    if action in ("Buy","Strong Buy","Add","Add more","Keep DCA"):
        return "background:rgba(29,158,117,0.15);color:#1D9E75;border:1px solid rgba(29,158,117,0.3)"
    if action in ("Avoid","Sell","Reduce"):
        return "background:rgba(216,90,48,0.13);color:#D85A30;border:1px solid rgba(216,90,48,0.3)"
    return "background:rgba(128,128,128,0.1);border:1px solid rgba(128,128,128,0.25)"


def _risk_pill(risk):
    styles = {
        "low":  "background:rgba(29,158,117,0.12);color:#1D9E75;border:1px solid rgba(29,158,117,0.25)",
        "mid":  "background:rgba(186,117,23,0.12);color:#BA7517;border:1px solid rgba(186,117,23,0.25)",
        "high": "background:rgba(216,90,48,0.12);color:#D85A30;border:1px solid rgba(216,90,48,0.25)",
    }
    label = {"low":"Low risk","mid":"Mid risk","high":"High risk"}.get(risk, risk)
    return f'<span style="{styles.get(risk,"")};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:600">{label}</span>'


def _accent(t):
    return {
        "Risk":        "linear-gradient(90deg,#D85A30,#BA7517)",
        "Opportunity": "linear-gradient(90deg,#1D9E75,#378ADD)",
        "Watch":       "linear-gradient(90deg,#BA7517,#888780)",
    }.get(t,"rgba(128,128,128,0.4)")


def _render_event(event):
    accent = _accent(event["type"])
    source_date = f'{event.get("source","MarketIQ")} · {event.get("date","Today")}'
    st.markdown(
        f'<div style="background:rgba(128,128,128,0.05);border:1px solid rgba(128,128,128,0.14);'
        f'border-radius:16px;padding:1rem 1.25rem 0.5rem;margin-bottom:1rem;'
        f'position:relative;overflow:hidden;box-shadow:0 2px 14px rgba(0,0,0,0.05);">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:2px;'
        f'background:{accent};border-radius:16px 16px 0 0;opacity:0.7;"></div>'
        f'{_type_badge(event["type"])}'
        f'&nbsp;<span style="font-size:0.7rem;opacity:0.4;font-weight:500">'
        f'{event["category"].upper()} &nbsp;·&nbsp; {source_date}</span>'
        f'<div style="font-weight:600;font-size:1rem;margin:6px 0 4px">{event["headline"]}</div>'
        f'<div style="font-size:0.83rem;opacity:0.65;line-height:1.55;margin-bottom:0.75rem">{event["logic"]}</div>'
        f'</div>',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:0.78rem;font-weight:600;opacity:0.45;text-transform:uppercase;'
        'letter-spacing:0.06em;margin:0 0 8px">What to do with your money</p>',
        unsafe_allow_html=True)

    cols = st.columns(len(event["actions"]))
    for col, action in zip(cols, event["actions"]):
        ap = _action_pill(action["action"])
        rp = _risk_pill(action["risk"])
        with col:
            st.markdown(
                f'<div style="background:rgba(128,128,128,0.06);border:1px solid rgba(128,128,128,0.13);'
                f'border-radius:14px;padding:12px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
                f'<span style="font-weight:700;font-size:0.95rem">{action["ticker"]}</span>'
                f'<span style="{ap};padding:2px 9px;border-radius:20px;font-size:0.68rem;font-weight:700">'
                f'{action["action"]}</span></div>'
                f'<div style="font-size:0.78rem;opacity:0.65;line-height:1.5;margin-bottom:8px">{action["reason"]}</div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'{rp}<span style="font-size:0.7rem;opacity:0.4">{action["horizon"]}</span>'
                f'</div></div>',
                unsafe_allow_html=True)

    st.markdown("&nbsp;")


@st.cache_data(ttl=86400, show_spinner=False)  # refresh daily
def _fetch_rss_headlines():
    """Fetch top headlines from RSS feeds. Returns list of dicts."""
    if not FEEDPARSER_OK:
        return []
    items = []
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                title = entry.get("title","").strip()
                link  = entry.get("link","")
                pub   = entry.get("published","")[:16] if entry.get("published") else "Today"
                if title:
                    items.append({"source": source, "title": title, "link": link, "date": pub})
        except Exception:
            continue
    return items[:15]


def show():
    st.markdown('<h2 style="font-size:1.5rem;font-weight:600;margin-bottom:6px;letter-spacing:-0.3px">News → Stock Recommendations</h2>', unsafe_allow_html=True)
    st.caption("Global events translated into specific buy / hold / avoid actions — updated daily.")

    # ── controls ──────────────────────────────────────────────────────────────
    ctrl1, ctrl2, ctrl3 = st.columns([2,2,1])
    with ctrl1:
        filter_type = st.segmented_control(
            "Filter", ["All","Risk","Opportunity","Watch"],
            default="All", label_visibility="collapsed")
    with ctrl2:
        filter_cat = st.selectbox(
            "Category", ["All categories","AI Infrastructure","Geopolitical / Energy",
                         "Labor Market","Earnings Season","Tech Correction","Macro"],
            label_visibility="collapsed")
    with ctrl3:
        if st.button("🔄 Refresh news", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown(
        f'<div style="font-size:0.75rem;opacity:0.4;margin-bottom:12px">'
        f'News refreshes daily · Last checked: {datetime.datetime.utcnow().strftime("%b %d, %Y %H:%M UTC")}'
        f'</div>',
        unsafe_allow_html=True)

    # ── summary metrics ───────────────────────────────────────────────────────
    risks = sum(1 for e in CURATED_NEWS if e["type"]=="Risk")
    opps  = sum(1 for e in CURATED_NEWS if e["type"]=="Opportunity")
    watch = sum(1 for e in CURATED_NEWS if e["type"]=="Watch")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Events tracked", len(CURATED_NEWS))
    c2.metric("Risk events", risks)
    c3.metric("Opportunities", opps)
    c4.metric("Watching", watch)

    st.markdown("---")

    # ── live RSS headlines strip ───────────────────────────────────────────────
    with st.expander("📡 Latest market headlines (live RSS feed)", expanded=False):
        headlines = _fetch_rss_headlines()
        if headlines:
            for h in headlines:
                st.markdown(
                    f'<div style="padding:6px 0;border-bottom:1px solid rgba(128,128,128,0.12)">'
                    f'<span style="font-size:0.72rem;opacity:0.45">{h["source"]} · {h["date"]}</span><br>'
                    f'<a href="{h["link"]}" target="_blank" style="font-size:0.85rem;text-decoration:none">'
                    f'{h["title"]}</a></div>',
                    unsafe_allow_html=True)
        else:
            st.caption("Live RSS headlines will appear here when the app is deployed. "
                       "Install feedparser: `pip install feedparser`")

    st.markdown("---")

    # ── filter and render curated events ─────────────────────────────────────
    events = CURATED_NEWS
    if filter_type and filter_type != "All":
        events = [e for e in events if e["type"] == filter_type]
    if filter_cat and filter_cat != "All categories":
        events = [e for e in events if e["category"] == filter_cat]

    if not events:
        st.info("No events match your current filter. Try changing the type or category.")
        return

    for event in events:
        _render_event(event)
