import streamlit as st
import datetime

try:
    import feedparser
    FEEDPARSER_OK = True
except ImportError:
    FEEDPARSER_OK = False

RSS_FEEDS = {
    "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
    "CNBC Top News":    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "Yahoo Finance":    "https://finance.yahoo.com/news/rssindex",
    "MarketWatch":      "https://feeds.content.dowjones.io/public/rss/mw_topstories",
}

CURATED_NEWS = [
    {
        "type": "Opportunity", "category": "AI Infrastructure",
        "headline": "AI capex spending by hyperscalers hits record $250B globally in 2026",
        "source": "CNBC", "date": "May 9, 2026",
        "logic": "Microsoft, Google, Amazon and Meta spending $250B on AI data centers. Largest capex cycle in tech history — winners span chips, power, cooling, and networking.",
        "actions": [
            {"ticker":"SOXX","action":"Strong Buy","risk":"mid","reason":"Entire semiconductor value chain benefits. NVDA, AMD, AVGO, TSM all held. Revenue +35% avg YoY.","horizon":"3–5 yrs"},
            {"ticker":"NVDA","action":"Strong Buy","risk":"high","reason":"80%+ AI chip share. Every AI dollar flows through Nvidia first. $280 analyst target.","horizon":"3–5 yrs"},
            {"ticker":"NEE","action":"Buy","risk":"low","reason":"AI data centers are fastest growing power consumer. NEE is largest US clean energy provider.","horizon":"5–10 yrs"},
            {"ticker":"EQIX","action":"Buy","risk":"mid","reason":"World's largest data center REIT. Physical AI infrastructure globally.","horizon":"5–10 yrs"},
        ],
    },
    {
        "type": "Opportunity", "category": "Labor Market",
        "headline": "US jobs beat by double: +115K in April vs 60K forecast",
        "source": "BLS / Schwab", "date": "May 8, 2026",
        "logic": "Two consecutive months of six-figure job growth signals a resilient economy. Strong labor supports consumer spending and corporate earnings.",
        "actions": [
            {"ticker":"VOO/SPY","action":"Buy","risk":"low","reason":"Strong economy = broad market upside. Keep DCA-ing into index funds.","horizon":"Long term"},
            {"ticker":"JPM","action":"Buy","risk":"mid","reason":"Banks benefit from strong economy. JPMorgan is highest quality in the sector.","horizon":"2–3 yrs"},
            {"ticker":"COST","action":"Buy","risk":"low","reason":"Consumer spending resilient despite oil shock. Membership model recession-resistant.","horizon":"3–5 yrs"},
            {"ticker":"TLT","action":"Hold","risk":"low","reason":"Delayed rate cuts means bonds stay pressured. Don't over-allocate long-duration.","horizon":"Watch Fed"},
        ],
    },
    {
        "type": "Risk", "category": "Geopolitical / Energy",
        "headline": "Oil above $100/barrel — economists warn of recession risk",
        "source": "CNBC / Morgan Stanley", "date": "May 6, 2026",
        "logic": "Oil up 50%+ since US-Iran conflict began Feb 28. Energy shock could trigger global recession if unresolved. Opportunities in defense and energy.",
        "actions": [
            {"ticker":"ITA","action":"Buy","risk":"low","reason":"Defense ETF. Government contracts locked in. NATO spending at record highs.","horizon":"2–4 yrs"},
            {"ticker":"XOM/CVX","action":"Buy","risk":"mid","reason":"Higher oil = higher profits. Natural hedge against geopolitical risk.","horizon":"During conflict"},
            {"ticker":"GLD","action":"Add","risk":"low","reason":"Safe haven in crisis. Allocate 5–10% max as insurance.","horizon":"Hold as hedge"},
            {"ticker":"Airlines","action":"Avoid","risk":"high","reason":"Jet fuel costs crushing margins. Avoid DAL, UAL until oil < $85.","horizon":"Stay away"},
        ],
    },
    {
        "type": "Watch", "category": "Earnings Season",
        "headline": "Mag 7 earnings beat: Meta +61% EPS, Amazon AWS reaccelerating",
        "source": "CNBC / Motley Fool", "date": "May 5–8, 2026",
        "logic": "Meta EPS up 61% YoY. AWS growing again. Google Search and Cloud beat. AI monetization showing up in actual earnings — not just promises.",
        "actions": [
            {"ticker":"META","action":"Buy","risk":"high","reason":"+61% EPS, $145B AI capex, lowest P/E of Mag 7 at 19.8x forward.","horizon":"2–4 yrs"},
            {"ticker":"AMZN","action":"Buy","risk":"mid","reason":"AWS reaccelerating is the key signal. Cloud = highest margin segment.","horizon":"3–5 yrs"},
            {"ticker":"GOOGL","action":"Buy","risk":"mid","reason":"Search + Cloud both beat. Gemini remonetizing core business.","horizon":"3–5 yrs"},
            {"ticker":"QQQM","action":"Buy","risk":"mid","reason":"All Mag 7 earnings beats flow through QQQM. Lower cost than QQQ.","horizon":"Long term"},
        ],
    },
    {
        "type": "Risk", "category": "Tech Correction",
        "headline": "Cloudflare drops 14% after 1,100 layoffs citing AI efficiency",
        "source": "Reuters / Schwab", "date": "May 8, 2026",
        "logic": "~100K tech workers laid off YTD. Companies using AI to cut headcount, compressing software valuations. Sector-wide signal.",
        "actions": [
            {"ticker":"NET","action":"Watch","risk":"high","reason":"14% drop on solid earnings may be overdone. Monitor for dip entry.","horizon":"Entry watch"},
            {"ticker":"CRWD/ZS","action":"Hold","risk":"high","reason":"Cybersecurity fundamentals strong. Hold existing, cautious adding.","horizon":"Monitor"},
            {"ticker":"MSFT","action":"Buy","risk":"low","reason":"Benefits from AI efficiency both ways — as provider and leaner operator.","horizon":"3–5 yrs"},
            {"ticker":"SOXX","action":"Buy","risk":"mid","reason":"Hardware/chip layer immune to SaaS margin compression.","horizon":"3–5 yrs"},
        ],
    },
]

def _type_badge(t):
    styles = {
        "Risk":        "background:rgba(216,90,48,0.13);color:#D85A30;border:0.5px solid rgba(216,90,48,0.3)",
        "Opportunity": "background:rgba(29,158,117,0.13);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.3)",
        "Watch":       "background:rgba(186,117,23,0.13);color:#BA7517;border:0.5px solid rgba(186,117,23,0.3)",
    }
    return f'<span style="{styles.get(t,"")};padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:700">{t}</span>'

def _action_pill(a):
    if a in ("Buy","Strong Buy","Add","Add more","Keep DCA"):
        return "background:rgba(29,158,117,0.15);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.3)"
    if a in ("Avoid","Sell","Reduce"):
        return "background:rgba(216,90,48,0.13);color:#D85A30;border:0.5px solid rgba(216,90,48,0.3)"
    return "background:rgba(128,128,128,0.1);border:0.5px solid rgba(128,128,128,0.25)"

def _risk_pill(r):
    p = {"low":"rgba(29,158,117,0.12);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.25)",
         "mid":"rgba(186,117,23,0.12);color:#BA7517;border:0.5px solid rgba(186,117,23,0.25)",
         "high":"rgba(216,90,48,0.12);color:#D85A30;border:0.5px solid rgba(216,90,48,0.25)"}
    label = {"low":"Low risk","mid":"Mid risk","high":"High risk"}.get(r,r)
    return f'<span style="background:{p.get(r,"rgba(128,128,128,0.1)")};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:600">{label}</span>'

def _accent(t):
    return {"Risk":"linear-gradient(90deg,#D85A30,#BA7517)","Opportunity":"linear-gradient(90deg,#1D9E75,#378ADD)","Watch":"linear-gradient(90deg,#BA7517,#888780)"}.get(t,"rgba(128,128,128,0.4)")

@st.cache_data(ttl=86400, show_spinner=False)
def _fetch_rss():
    if not FEEDPARSER_OK:
        return []
    items = []
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:3]:
                title = e.get("title","").strip()
                link  = e.get("link","")
                pub   = e.get("published","")[:16] if e.get("published") else "Today"
                if title:
                    items.append({"source":source,"title":title,"link":link,"date":pub})
        except Exception:
            continue
    return items[:15]

def show():
    st.markdown('<h2 style="font-size:1.5rem;font-weight:600;letter-spacing:-0.3px;margin-bottom:4px">News → Stock Recommendations</h2>', unsafe_allow_html=True)
    st.caption("Global events translated into specific buy / hold / avoid actions — updated daily.")

    c1,c2,c3 = st.columns([2,2,1])
    with c1:
        filter_type = st.segmented_control("Filter",["All","Risk","Opportunity","Watch"],default="All",label_visibility="collapsed")
    with c2:
        filter_cat = st.selectbox("Category",["All categories","AI Infrastructure","Geopolitical / Energy","Labor Market","Earnings Season","Tech Correction","Macro"],label_visibility="collapsed")
    with c3:
        if st.button("🔄 Refresh news",use_container_width=True):
            st.cache_data.clear(); st.rerun()

    st.markdown(f'<div style="font-size:0.75rem;opacity:0.4;margin-bottom:12px">Refreshes daily · Checked: {datetime.datetime.utcnow().strftime("%b %d, %Y %H:%M UTC")}</div>',unsafe_allow_html=True)

    risks=sum(1 for e in CURATED_NEWS if e["type"]=="Risk")
    opps=sum(1 for e in CURATED_NEWS if e["type"]=="Opportunity")
    watch=sum(1 for e in CURATED_NEWS if e["type"]=="Watch")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Events",len(CURATED_NEWS)); c2.metric("Risks",risks); c3.metric("Opportunities",opps); c4.metric("Watching",watch)
    st.markdown("---")

    with st.expander("📡 Latest market headlines (live RSS)", expanded=False):
        headlines = _fetch_rss()
        if headlines:
            for h in headlines:
                st.markdown(f'<div style="padding:6px 0;border-bottom:0.5px solid rgba(128,128,128,0.12)"><span style="font-size:0.72rem;opacity:0.45">{h["source"]} · {h["date"]}</span><br><a href="{h["link"]}" target="_blank" style="font-size:0.85rem;text-decoration:none">{h["title"]}</a></div>',unsafe_allow_html=True)
        else:
            st.caption("Install feedparser for live RSS: `pip install feedparser`")

    st.markdown("---")
    events = CURATED_NEWS
    if filter_type and filter_type != "All":
        events = [e for e in events if e["type"]==filter_type]
    if filter_cat and filter_cat != "All categories":
        events = [e for e in events if e["category"]==filter_cat]
    if not events:
        st.info("No events match your filter."); return

    for event in events:
        st.markdown(
            f'<div style="background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.14);border-radius:16px;padding:1rem 1.25rem 0.5rem;margin-bottom:1rem;position:relative;overflow:hidden;">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;background:{_accent(event["type"])};border-radius:16px 16px 0 0;opacity:0.7"></div>'
            f'{_type_badge(event["type"])}&nbsp;<span style="font-size:0.7rem;opacity:0.4;font-weight:500">{event["category"].upper()} · {event.get("source","")} · {event.get("date","")}</span>'
            f'<div style="font-weight:600;font-size:1rem;margin:6px 0 4px">{event["headline"]}</div>'
            f'<div style="font-size:0.83rem;opacity:0.65;line-height:1.55;margin-bottom:0.75rem">{event["logic"]}</div></div>',
            unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.78rem;font-weight:600;opacity:0.45;text-transform:uppercase;letter-spacing:0.06em;margin:0 0 8px">What to do with your money</p>',unsafe_allow_html=True)
        cols=st.columns(len(event["actions"]))
        for col,action in zip(cols,event["actions"]):
            with col:
                st.markdown(
                    f'<div style="background:rgba(128,128,128,0.06);border:0.5px solid rgba(128,128,128,0.13);border-radius:14px;padding:12px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><span style="font-weight:700;font-size:0.95rem">{action["ticker"]}</span><span style="{_action_pill(action["action"])};padding:2px 9px;border-radius:20px;font-size:0.68rem;font-weight:700">{action["action"]}</span></div>'
                    f'<div style="font-size:0.78rem;opacity:0.65;line-height:1.5;margin-bottom:8px">{action["reason"]}</div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">{_risk_pill(action["risk"])}<span style="font-size:0.7rem;opacity:0.4">{action["horizon"]}</span></div></div>',
                    unsafe_allow_html=True)
        st.markdown("&nbsp;")
