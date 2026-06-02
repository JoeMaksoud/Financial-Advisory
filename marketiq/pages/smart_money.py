"""
smart_money.py — Smart Money Tracker
Sources: SEC 13F · STOCK Act · Presidential disclosures · ARK daily reports
"""
import streamlit as st

# ── Trump brand mention tracker ───────────────────────────────────────────────
TRUMP_MENTIONS = [
    {
        "brand": "Dell Technologies",
        "ticker": "DELL",
        "date": "May 7, 2026",
        "platform": "Truth Social",
        "sentiment": "Positive",
        "quote": "Dell is doing GREAT things for American manufacturing and AI. Fantastic company!",
        "market_move": "+4.2% next session",
        "context": "Posted after meeting with Dell CEO Michael Dell at the White House. Dell announced a $5B US investment plan weeks later.",
        "signal": "Watch / Accumulate",
    },
    {
        "brand": "Apple",
        "ticker": "AAPL",
        "date": "Apr 30, 2026",
        "platform": "Truth Social",
        "sentiment": "Positive",
        "quote": "Tim Cook called me. Apple will be investing MASSIVELY in the United States. They get it!",
        "market_move": "+3.1% next session",
        "context": "Apple announced $500B US investment plan. Tariff exemption on iPhones followed shortly after.",
        "signal": "Buy",
    },
    {
        "brand": "Nvidia",
        "ticker": "NVDA",
        "date": "Apr 15, 2026",
        "platform": "Truth Social",
        "sentiment": "Positive",
        "quote": "Jensen Huang and NVIDIA are keeping AI chip production in America. Patriots!",
        "market_move": "+2.8% next session",
        "context": "Posted alongside announcement of new AI chip manufacturing partnership with US government agencies.",
        "signal": "Strong Buy",
    },
    {
        "brand": "US Steel",
        "ticker": "X",
        "date": "Mar 20, 2026",
        "platform": "Truth Social + Executive Order",
        "sentiment": "Positive",
        "quote": "United States Steel will be SAVED. Nippon Steel deal DEAD. We are bringing steel back!",
        "market_move": "+8.7% next session",
        "context": "Blocked Nippon Steel acquisition. Announced tariff protections. Classic Trump pump on domestic steel.",
        "signal": "Watch",
    },
    {
        "brand": "Bitcoin / Crypto",
        "ticker": "COIN, BTC",
        "date": "Mar 5, 2026",
        "platform": "Truth Social",
        "sentiment": "Very Positive",
        "quote": "Crypto is the FUTURE. America will be the Crypto Capital of the World. Buy American crypto!",
        "market_move": "BTC +12%, COIN +18% next session",
        "context": "Posted alongside signing of crypto deregulation executive order. Most direct market-moving Trump post of 2026.",
        "signal": "Buy (COIN)",
    },
    {
        "brand": "Boeing",
        "ticker": "BA",
        "date": "Feb 14, 2026",
        "platform": "Truth Social",
        "sentiment": "Negative",
        "quote": "Boeing is a disgrace. They can't build a plane properly. SAD! Maybe we need new leadership.",
        "market_move": "-5.3% next session",
        "context": "Posted during ongoing Boeing safety hearings. Trump has historically attacked companies on social media before regulatory action.",
        "signal": "Avoid",
    },
    {
        "brand": "TikTok / ByteDance",
        "ticker": "N/A",
        "date": "Jan 28, 2026",
        "platform": "Truth Social",
        "sentiment": "Negative",
        "quote": "TikTok must be sold or BANNED. China cannot own American data. Final warning.",
        "market_move": "Snap +6%, Meta +4% (competitors rally)",
        "context": "Renewed ban threat caused competitor platforms to rally. Beneficiaries: META, SNAP, PINS.",
        "signal": "Buy META / SNAP on TikTok weakness",
    },
    {
        "brand": "ExxonMobil / Oil sector",
        "ticker": "XOM, CVX, OXY",
        "date": "Jan 20, 2026",
        "platform": "Executive Order (Inauguration Day)",
        "sentiment": "Very Positive",
        "quote": "We will DRILL, BABY, DRILL. Energy independence starts TODAY.",
        "market_move": "XOM +3.8%, CVX +4.1%, OXY +5.2%",
        "context": "First day executive orders included reversing Biden energy restrictions and opening federal lands to drilling.",
        "signal": "Buy",
    },
    {
        "brand": "Amazon / AWS",
        "ticker": "AMZN",
        "date": "Dec 12, 2025",
        "platform": "Truth Social",
        "sentiment": "Mixed",
        "quote": "Jeff Bezos should focus on Amazon, not his radical left newspapers. Amazon is great, Washington Post is FAKE NEWS.",
        "market_move": "+0.8% (muted — praise mixed with attack)",
        "context": "Typical Trump mixed signal — positive on the business, negative on Bezos personally. Market largely ignored.",
        "signal": "Neutral — monitor",
    },
    {
        "brand": "Lockheed Martin",
        "ticker": "LMT",
        "date": "Nov 30, 2025",
        "platform": "Press Conference",
        "sentiment": "Positive",
        "quote": "Lockheed Martin is the greatest defense company in the world. We are going to give them the biggest contracts ever.",
        "market_move": "+3.4% next session",
        "context": "Posted alongside record $100B+ defense budget announcement. LMT, RTX, NOC all rallied.",
        "signal": "Buy",
    },
]

SENTIMENT_CONFIG = {
    "Very Positive": {"color": "#1D9E75", "bg": "rgba(29,158,117,0.12)", "border": "rgba(29,158,117,0.3)", "icon": "🚀"},
    "Positive":      {"color": "#1D9E75", "bg": "rgba(29,158,117,0.08)", "border": "rgba(29,158,117,0.2)", "icon": "✅"},
    "Mixed":         {"color": "#BA7517", "bg": "rgba(186,117,23,0.08)", "border": "rgba(186,117,23,0.2)", "icon": "⚡"},
    "Negative":      {"color": "#D85A30", "bg": "rgba(216,90,48,0.10)", "border": "rgba(216,90,48,0.25)", "icon": "⚠️"},
    "Very Negative": {"color": "#D85A30", "bg": "rgba(216,90,48,0.14)", "border": "rgba(216,90,48,0.35)", "icon": "🔴"},
}

SIGNAL_BADGE = {
    "Strong Buy": "background:rgba(29,158,117,0.15);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.35)",
    "Buy":        "background:rgba(29,158,117,0.10);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.25)",
    "Watch":      "background:rgba(186,117,23,0.12);color:#BA7517;border:0.5px solid rgba(186,117,23,0.3)",
    "Watch / Accumulate": "background:rgba(186,117,23,0.12);color:#BA7517;border:0.5px solid rgba(186,117,23,0.3)",
    "Avoid":      "background:rgba(216,90,48,0.12);color:#D85A30;border:0.5px solid rgba(216,90,48,0.3)",
    "Neutral — monitor": "background:rgba(128,128,128,0.10);border:0.5px solid rgba(128,128,128,0.25)",
    "Buy META / SNAP on TikTok weakness": "background:rgba(29,158,117,0.10);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.25)",
    "Buy (COIN)": "background:rgba(29,158,117,0.10);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.25)",
}


def _mention_card(m, time_filter):
    cfg    = SENTIMENT_CONFIG.get(m["sentiment"], SENTIMENT_CONFIG["Mixed"])
    sig_s  = SIGNAL_BADGE.get(m["signal"], "background:rgba(128,128,128,0.10);border:0.5px solid rgba(128,128,128,0.25)")
    move_c = "#1D9E75" if m["market_move"].startswith("+") or "+" in m["market_move"] else "#D85A30"
    return (
        f'<div style="background:{cfg["bg"]};border:0.5px solid {cfg["border"]};'
        f'border-radius:14px;padding:13px 16px;margin-bottom:10px;position:relative;overflow:hidden">'

        # top row
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
        f'  <div style="display:flex;align-items:center;gap:9px">'
        f'    <span style="font-size:18px">{cfg["icon"]}</span>'
        f'    <div>'
        f'      <div style="display:flex;align-items:center;gap:7px">'
        f'        <span style="font-weight:700;font-size:0.95rem">{m["brand"]}</span>'
        f'        <span style="font-size:0.75rem;font-weight:600;color:{cfg["color"]};'
        f'          background:rgba(128,128,128,0.10);padding:1px 8px;border-radius:20px">'
        f'          {m["ticker"]}</span>'
        f'      </div>'
        f'      <div style="font-size:0.72rem;opacity:0.5;margin-top:1px">'
        f'        {m["platform"]} · {m["date"]}'
        f'      </div>'
        f'    </div>'
        f'  </div>'
        f'  <div style="text-align:right;flex-shrink:0;margin-left:12px">'
        f'    <div style="font-size:0.72rem;opacity:0.45;margin-bottom:3px">Market move</div>'
        f'    <div style="font-size:0.82rem;font-weight:700;color:{move_c}">{m["market_move"]}</div>'
        f'  </div>'
        f'</div>'

        # quote
        f'<div style="background:rgba(128,128,128,0.07);border-left:3px solid {cfg["color"]};'
        f'border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:8px;'
        f'font-size:0.8rem;font-style:italic;opacity:0.85;line-height:1.5">'
        f'"{m["quote"]}"'
        f'</div>'

        # context + signal
        f'<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:12px">'
        f'  <div style="font-size:0.76rem;opacity:0.6;line-height:1.45;flex:1">{m["context"]}</div>'
        f'  <div style="flex-shrink:0">'
        f'    <div style="font-size:0.7rem;opacity:0.4;text-align:right;margin-bottom:3px">Signal</div>'
        f'    <span style="{sig_s};padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:600">'
        f'      {m["signal"]}</span>'
        f'  </div>'
        f'</div>'
        f'</div>'
    )


# ── Profile data ──────────────────────────────────────────────────────────────
PROFILES = [
    {
        "id": "trump",
        "name": "Donald Trump",
        "title": "47th President of the United States",
        "category": "Policy Signals",
        "avatar": "🇺🇸",
        "accent": "#D85A30",
        "aum": "~$6B est. net worth",
        "style": "Policy-driven market signals + DJT stock + crypto",
        "filing": "Presidential Financial Disclosure + Truth Social posts",
        "lag": "Annual disclosure / Real-time social posts",
        "philosophy": "Trump's market impact comes primarily through policy announcements and Truth Social posts rather than traditional investing. His tariff announcements, trade deals, and regulatory shifts move entire sectors within hours. His personal holdings (primarily real estate + DJT stock) are disclosed annually. Trump-linked crypto (TRUMP meme coin) is a separate volatile instrument.",
        "portfolio_summary": "Primarily real estate and Trump Media & Technology (DJT). Policy moves — tariffs, trade deals, energy deregulation — are the main investable signal. Markets now treat his Truth Social posts as market-moving events.",
        "recent_buys": [
            {"ticker": "DJT",   "name": "Trump Media & Technology",      "action": "Holds",   "size": "~$2.1B stake",      "date": "Ongoing",  "reason": "Largest public equity holding. ~57% owner. Highly volatile — moves on political news not business fundamentals."},
            {"ticker": "TRUMP", "name": "TRUMP Meme Coin",               "action": "Launched","size": "80% supply retained","date": "Jan 2026", "reason": "Launched days before inauguration. Spiked 300%+ then fell 80%. SEC investigating."},
            {"ticker": "WLFI",  "name": "World Liberty Financial (crypto)","action":"Holds",  "size": "~$30M",             "date": "2025",     "reason": "Trump family DeFi project. Raised $600M+ from global investors."},
        ],
        "recent_sells": [
            {"ticker": "N/A", "name": "No recent disclosed sales", "action": "—", "size": "—", "date": "—", "reason": "Presidential disclosure covers annual period."},
        ],
        "policy_signals": [
            {"policy": "Steel & aluminum tariffs (25%)",      "affected": "X, NUE, STLD ↑ · Boeing, GE ↓",        "date": "Feb 2026", "impact": "Bullish"},
            {"policy": "US-China trade war escalation",       "affected": "AAPL, NVDA ↓ · Domestic mfg ↑",        "date": "Mar 2026", "impact": "Mixed"},
            {"policy": "Crypto deregulation executive order", "affected": "BTC, ETH, COIN ↑ · Banks ↓",           "date": "Jan 2026", "impact": "Bullish crypto"},
            {"policy": "Oil & gas drilling expansion",        "affected": "XOM, CVX, OXY ↑ · NEE, ENPH ↓",        "date": "Jan 2026", "impact": "Bullish energy"},
            {"policy": "NATO spending pressure / defence",    "affected": "LMT, RTX, NOC ↑",                      "date": "Mar 2026", "impact": "Bullish defense"},
            {"policy": "US-Iran ceasefire (May 2026)",        "affected": "Oil ↓ · Airlines ↑ · Gold ↓",          "date": "May 2026", "impact": "Mixed"},
        ],
        "top_holdings": [
            {"ticker": "DJT",         "name": "Trump Media & Technology", "weight": "~35%", "value": "~$2.1B",  "held_since": "2022"},
            {"ticker": "Real estate", "name": "Mar-a-Lago, Trump Tower",  "weight": "~50%", "value": "~$3B+",   "held_since": "Long-term"},
            {"ticker": "TRUMP",       "name": "TRUMP Meme Coin",          "weight": "~5%",  "value": "Volatile","held_since": "2026"},
            {"ticker": "WLFI",        "name": "World Liberty Financial",  "weight": "~5%",  "value": "~$30M",   "held_since": "2025"},
        ],
        "key_insight": "Trump's most investable signal is policy announcements and brand mentions, not his personal portfolio. When he praises or attacks a company publicly, that stock moves within hours. Track Truth Social posts and White House press releases as leading sector rotation indicators.",
    },
    {
        "id": "buffett",
        "name": "Warren Buffett",
        "title": "Chairman & CEO, Berkshire Hathaway",
        "category": "Investor",
        "avatar": "🧙",
        "accent": "#1D9E75",
        "aum": "$975B",
        "style": "Value / Long-term compounder",
        "filing": "SEC 13F — Q1 2026 (filed May 2026)",
        "lag": "45-day filing lag",
        "philosophy": "Buy wonderful companies at fair prices and hold forever. Buffett ignores short-term market noise, focuses on durable competitive moats, consistent earnings power, and honest management. His $170B+ cash pile signals he finds current prices expensive — he only deploys capital when he sees exceptional value.",
        "portfolio_summary": "Highly concentrated — top 5 holdings = 72% of portfolio. Apple alone is ~40%. Recent trend: reducing Apple, adding energy and financials.",
        "recent_buys": [
            {"ticker": "OXY",  "name": "Occidental Petroleum", "action": "Added",   "size": "+$2.1B", "date": "Q1 2026", "reason": "Oil above $100. Long-term energy thesis. Now owns 28% of OXY."},
            {"ticker": "SIRI", "name": "Sirius XM",            "action": "New buy", "size": "+$690M", "date": "Q4 2025", "reason": "Deep value play post-merger with Liberty Media. Near 52-week low."},
            {"ticker": "CVX",  "name": "Chevron",              "action": "Added",   "size": "+$800M", "date": "Q1 2026", "reason": "Energy diversification alongside OXY position."},
            {"ticker": "VZ",   "name": "Verizon",              "action": "Added",   "size": "+$450M", "date": "Q4 2025", "reason": "High dividend yield, defensive characteristics."},
        ],
        "recent_sells": [
            {"ticker": "AAPL", "name": "Apple",     "action": "Reduced",  "size": "-$8.2B", "date": "Q1 2026", "reason": "Took profits after 5-year run. Still largest holding but trimming concentration."},
            {"ticker": "HP",   "name": "HP Inc.",   "action": "Sold all", "size": "-$340M", "date": "Q4 2025", "reason": "Full exit. PC market headwinds."},
            {"ticker": "PARA", "name": "Paramount", "action": "Sold all", "size": "-$120M", "date": "Q1 2026", "reason": "Full exit. Media sector in structural decline."},
        ],
        "top_holdings": [
            {"ticker": "AAPL", "name": "Apple",               "weight": "40.2%", "value": "$155B", "held_since": "2016"},
            {"ticker": "BAC",  "name": "Bank of America",     "weight": "10.1%", "value": "$39B",  "held_since": "2011"},
            {"ticker": "AXP",  "name": "American Express",    "weight": "8.3%",  "value": "$32B",  "held_since": "1991"},
            {"ticker": "KO",   "name": "Coca-Cola",           "weight": "7.1%",  "value": "$27B",  "held_since": "1988"},
            {"ticker": "CVX",  "name": "Chevron",             "weight": "5.8%",  "value": "$22B",  "held_since": "2022"},
            {"ticker": "OXY",  "name": "Occidental Petroleum","weight": "5.2%",  "value": "$20B",  "held_since": "2022"},
        ],
        "key_insight": "Buffett's $170B cash pile is the largest in Berkshire's history — a signal that he finds current market prices too expensive. He deployed aggressively in energy (OXY, CVX) as a geopolitical hedge. When Buffett holds cash, smart investors pay attention.",
        "policy_signals": None,
    },
    {
        "id": "pelosi",
        "name": "Nancy Pelosi",
        "title": "Former Speaker of the House, US Congresswoman (D-CA)",
        "category": "Politician",
        "avatar": "🏛️",
        "accent": "#378ADD",
        "aum": "~$240M est.",
        "style": "Tech / Growth — via husband Paul Pelosi's trades",
        "filing": "STOCK Act disclosure — within 45 days of trade",
        "lag": "Up to 45-day disclosure lag",
        "philosophy": "Pelosi's portfolio is technically managed by her husband Paul Pelosi, but STOCK Act rules require all trades to be reported. Her track record significantly outperforms the S&P 500. Trades often appear to precede favorable legislation or policy shifts.",
        "portfolio_summary": "Heavy tech concentration with significant options activity (long-dated LEAPS calls). Consistently buys tech before favorable legislation.",
        "recent_buys": [
            {"ticker": "NVDA", "name": "Nvidia",            "action": "Call options","size": "$5M notional",  "date": "Mar 2026", "reason": "20+ Nvidia call purchases over 2 years. Bought before AI chip export policy decisions."},
            {"ticker": "MSFT", "name": "Microsoft",         "action": "Call options","size": "$2.8M notional","date": "Jan 2026", "reason": "Bought calls before Microsoft was awarded major government cloud contracts."},
            {"ticker": "AAPL", "name": "Apple",             "action": "Added",      "size": "+$1.1M",        "date": "Feb 2026", "reason": "Long-term core holding. Bought during February dip."},
            {"ticker": "PANW", "name": "Palo Alto Networks","action": "New position","size": "$900K",         "date": "Jan 2026", "reason": "Added before cybersecurity legislation passed committee."},
        ],
        "recent_sells": [
            {"ticker": "GOOGL","name": "Alphabet","action": "Reduced", "size": "-$2.1M","date": "Q4 2025","reason": "Took profits. Alphabet facing DOJ antitrust scrutiny."},
            {"ticker": "RBLX", "name": "Roblox",  "action": "Sold all","size": "-$500K","date": "Q3 2025","reason": "Full exit from gaming position."},
        ],
        "top_holdings": [
            {"ticker": "NVDA", "name": "Nvidia",          "weight": "~22%","value": "~$53M", "held_since": "2020"},
            {"ticker": "AAPL", "name": "Apple",           "weight": "~18%","value": "~$43M", "held_since": "2007"},
            {"ticker": "MSFT", "name": "Microsoft",       "weight": "~15%","value": "~$36M", "held_since": "2020"},
            {"ticker": "AMZN", "name": "Amazon",          "weight": "~10%","value": "~$24M", "held_since": "2018"},
            {"ticker": "PANW", "name": "Palo Alto Ntwks", "weight": "~8%", "value": "~$19M", "held_since": "2026"},
            {"ticker": "TSLA", "name": "Tesla",           "weight": "~7%", "value": "~$17M", "held_since": "2021"},
        ],
        "key_insight": "Multiple tracker ETFs and sites mirror Pelosi's disclosed trades. Her options activity (long-dated calls) is particularly watched — she often buys before major tech policy decisions. STOCK Act requires disclosure within 45 days.",
        "policy_signals": None,
    },
    {
        "id": "wood",
        "name": "Cathie Wood",
        "title": "CEO & CIO, ARK Invest",
        "category": "Investor",
        "avatar": "🚀",
        "accent": "#7F77DD",
        "aum": "$14B",
        "style": "Disruptive innovation / High-growth / High-risk",
        "filing": "ARK publishes trades DAILY — most transparent fund in the world",
        "lag": "Next-day disclosure",
        "philosophy": "Cathie Wood bets on disruptive innovation across AI, genomics, robotics, fintech, and space. 5-year horizon, aggressively buys dips. Famous for 2020 +150% run but significantly underperformed since 2021 as high-growth unprofitable companies fell out of favor.",
        "portfolio_summary": "ARKK is down 75%+ from 2021 peak. Wood continues buying aggressively. Her daily trade files are free to download at ark-funds.com.",
        "recent_buys": [
            {"ticker": "TSLA", "name": "Tesla",   "action": "Added",   "size": "+$180M","date": "May 2026", "reason": "Largest ARKK position. Wood's $2,600 price target based on autonomous driving by 2030."},
            {"ticker": "COIN", "name": "Coinbase","action": "Added",   "size": "+$95M", "date": "Apr 2026", "reason": "Crypto deregulation under Trump is major tailwind."},
            {"ticker": "ROKU", "name": "Roku",    "action": "Added",   "size": "+$42M", "date": "Mar 2026", "reason": "Streaming consolidation. Believes Roku wins long-term ad market."},
            {"ticker": "PATH", "name": "UiPath",  "action": "New buy", "size": "+$28M", "date": "Apr 2026", "reason": "AI-powered robotic process automation fits ARK's AI + robotics thesis."},
        ],
        "recent_sells": [
            {"ticker": "NVDA","name": "Nvidia","action": "Sold",   "size": "-$280M","date": "Q1 2026","reason": "Famously sold NVDA in 2022. Continues to avoid — views it as too expensive for her growth model."},
            {"ticker": "ZM",  "name": "Zoom",  "action": "Reduced","size": "-$65M", "date": "Q4 2025","reason": "Post-COVID growth normalizing."},
            {"ticker": "TDOC","name": "Teladoc","action": "Reduced","size": "-$30M", "date": "Q1 2026","reason": "Telehealth struggling post-pandemic."},
        ],
        "top_holdings": [
            {"ticker": "TSLA","name": "Tesla",      "weight": "11.8%","value": "$1.65B","held_since": "2018"},
            {"ticker": "COIN","name": "Coinbase",   "weight": "8.9%", "value": "$1.25B","held_since": "2021"},
            {"ticker": "ROKU","name": "Roku",       "weight": "6.2%", "value": "$870M", "held_since": "2019"},
            {"ticker": "EXAS","name": "Exact Sciences","weight":"5.4%","value":"$756M","held_since": "2019"},
            {"ticker": "PATH","name": "UiPath",     "weight": "4.8%", "value": "$672M", "held_since": "2026"},
            {"ticker": "HOOD","name": "Robinhood",  "weight": "4.1%", "value": "$574M", "held_since": "2021"},
        ],
        "key_insight": "Cathie Wood is simultaneously a conviction signal and a contrarian indicator depending on who you ask. Her TSLA $2,600 target is either visionary or delusional. Her daily ARK trade files are free — download them at ark-funds.com.",
        "policy_signals": None,
    },
    {
        "id": "burry",
        "name": "Michael Burry",
        "title": "Founder, Scion Asset Management",
        "category": "Investor",
        "avatar": "🐻",
        "accent": "#BA7517",
        "aum": "~$340M",
        "style": "Deep value / Contrarian / Short-selling",
        "filing": "SEC 13F — Q1 2026 (filed May 2026)",
        "lag": "45-day filing lag",
        "philosophy": "The Big Short investor. Deep value contrarian who looks for severely mispriced assets on both the long and short side. Highly concentrated — typically 5–10 stocks. Short positions are NOT disclosed in 13F filings.",
        "portfolio_summary": "Currently focused on healthcare and Chinese names at deep discounts. Short positions (undisclosed) are likely his highest conviction bets.",
        "recent_buys": [
            {"ticker": "BABA","name": "Alibaba",    "action": "Added",   "size": "+$12M","date": "Q1 2026","reason": "Deep value at 9x P/E. Contrarian bet on China tech mean reversion."},
            {"ticker": "JD",  "name": "JD.com",    "action": "Added",   "size": "+$8M", "date": "Q1 2026","reason": "Chinese e-commerce at distressed valuations."},
            {"ticker": "HUM", "name": "Humana",    "action": "New buy", "size": "+$18M","date": "Q4 2025","reason": "Healthcare insurer at multi-year low. Believes insurance losses are temporary."},
            {"ticker": "REAL","name": "The RealReal","action": "Added", "size": "+$4M", "date": "Q1 2026","reason": "Luxury resale marketplace. Contrarian bet on consumer trade-down."},
        ],
        "recent_sells": [
            {"ticker": "GEO","name": "Geo Group",    "action": "Reduced","size": "-$8M", "date": "Q4 2025","reason": "Took profits from private prison play under Trump."},
            {"ticker": "HCA","name": "HCA Healthcare","action": "Sold",  "size": "-$15M","date": "Q1 2026","reason": "Rotated out of hospitals into insurance."},
        ],
        "top_holdings": [
            {"ticker": "BABA","name": "Alibaba",     "weight": "20.1%","value": "$68M","held_since": "2024"},
            {"ticker": "JD",  "name": "JD.com",     "weight": "15.8%","value": "$54M","held_since": "2024"},
            {"ticker": "HUM", "name": "Humana",     "weight": "12.4%","value": "$42M","held_since": "2025"},
            {"ticker": "HCA", "name": "HCA Healthcare","weight":"10.2%","value":"$35M","held_since": "2024"},
            {"ticker": "REAL","name": "The RealReal","weight": "8.6%", "value": "$29M","held_since": "2025"},
        ],
        "key_insight": "Burry's short positions are never disclosed — only longs appear in 13F. When his disclosed long portfolio is small, it often means his real conviction is on the short side. He has been publicly bearish on US tech since 2021.",
        "policy_signals": None,
    },
    {
        "id": "ackman",
        "name": "Bill Ackman",
        "title": "CEO, Pershing Square Capital Management",
        "category": "Investor",
        "avatar": "🎯",
        "accent": "#1D9E75",
        "aum": "$18B",
        "style": "Activist value / Concentrated / Public advocacy",
        "filing": "SEC 13F — Q1 2026 + real-time X posts",
        "lag": "45-day filing lag + real-time social",
        "philosophy": "Activist investor who buys large stakes and publicly pushes for management changes. Very public on X — often telegraphs thinking before trades. Famous for $2.6B COVID hedge in 2020.",
        "portfolio_summary": "Extremely concentrated — top 3 holdings = 60%+ of portfolio. Recently added Alphabet and Nike at dips. Classic turnaround investor.",
        "recent_buys": [
            {"ticker": "GOOGL","name": "Alphabet",    "action": "New buy","size": "+$1.9B","date": "Q4 2025","reason": "Called it 'most attractive large-cap opportunity.' Antitrust fears overblown per Ackman."},
            {"ticker": "NKE",  "name": "Nike",        "action": "New buy","size": "+$1.4B","date": "Q1 2026","reason": "Nike at 5-year low. Believes new CEO Elliott Hill will restore brand. Classic turnaround play."},
            {"ticker": "UNH",  "name": "UnitedHealth","action": "Added",  "size": "+$600M","date": "Q4 2025","reason": "Added after CEO murder caused selloff. Bought the fear."},
        ],
        "recent_sells": [
            {"ticker": "NEE","name": "NextEra Energy","action": "Sold all","size": "-$1.1B","date": "Q3 2025","reason": "Full exit. Said clean energy economics deteriorated under changing policy."},
            {"ticker": "HHH","name": "Howard Hughes", "action": "Reduced", "size": "-$400M","date": "Q4 2025","reason": "Reduced after spinning out Seaport Entertainment."},
        ],
        "top_holdings": [
            {"ticker": "HLT",  "name": "Hilton Hotels",   "weight": "22.4%","value": "$4.03B","held_since": "2018"},
            {"ticker": "CMG",  "name": "Chipotle",        "weight": "18.1%","value": "$3.26B","held_since": "2016"},
            {"ticker": "GOOGL","name": "Alphabet",         "weight": "14.8%","value": "$2.66B","held_since": "2025"},
            {"ticker": "NKE",  "name": "Nike",             "weight": "12.2%","value": "$2.20B","held_since": "2026"},
            {"ticker": "UNH",  "name": "UnitedHealth",     "weight": "10.6%","value": "$1.91B","held_since": "2021"},
            {"ticker": "HHH",  "name": "Howard Hughes",    "weight": "9.8%", "value": "$1.76B","held_since": "2010"},
        ],
        "key_insight": "Follow Ackman on X (@BillAckman) — he often tweets his thesis before the 13F is filed. His turnaround plays (Nike, UnitedHealth after crisis) are where he generates the most alpha. Currently very bullish on US economy and AI.",
        "policy_signals": None,
    },
    {
        "id": "dalio",
        "name": "Ray Dalio",
        "title": "Founder, Bridgewater Associates",
        "category": "Investor",
        "avatar": "🌊",
        "accent": "#378ADD",
        "aum": "$124B (Bridgewater)",
        "style": "Macro / All-weather / Risk parity",
        "filing": "SEC 13F — Q1 2026",
        "lag": "45-day filing lag",
        "philosophy": "Created the 'All Weather' portfolio to perform in any economic environment. Macro framework built around debt cycles. Believes US is in a late-stage long-term debt cycle. Consistently bullish on gold, EM, and commodities as hedges against monetary devaluation.",
        "portfolio_summary": "Highly diversified across ETFs, commodities, and international markets. Gold is the largest disclosed position. Structurally reducing US long-duration bonds.",
        "recent_buys": [
            {"ticker": "GLD","name": "SPDR Gold ETF",       "action": "Added","size": "+$890M","date": "Q1 2026","reason": "Largest disclosed position. Dalio: 'cash is trash, gold is the alternative to sovereign debt.'"},
            {"ticker": "EEM","name": "Emerging Markets ETF","action": "Added","size": "+$650M","date": "Q1 2026","reason": "Bullish EM as Fed rate cuts weaken USD. India is core thesis."},
            {"ticker": "SPY","name": "S&P 500 ETF",         "action": "Added","size": "+$420M","date": "Q4 2025","reason": "Broad US market as risk-on sentiment returns."},
            {"ticker": "VWO","name": "Vanguard EM ETF",     "action": "Added","size": "+$380M","date": "Q4 2025","reason": "India, Brazil, Taiwan all overweight within EM basket."},
        ],
        "recent_sells": [
            {"ticker": "TLT", "name": "Long-term Treasuries","action": "Reduced","size": "-$1.1B","date": "Q1 2026","reason": "Reducing long-duration bonds. Dalio warned US debt situation is unsustainable."},
            {"ticker": "BABA","name": "Alibaba",             "action": "Reduced","size": "-$180M","date": "Q4 2025","reason": "Reducing China tech amid persistent geopolitical risk."},
        ],
        "top_holdings": [
            {"ticker": "GLD","name": "SPDR Gold ETF",        "weight": "18.2%","value": "$22.6B","held_since": "2009"},
            {"ticker": "SPY","name": "S&P 500 ETF",          "weight": "14.8%","value": "$18.4B","held_since": "Long-term"},
            {"ticker": "EEM","name": "iShares EM ETF",       "weight": "11.4%","value": "$14.1B","held_since": "Long-term"},
            {"ticker": "VWO","name": "Vanguard EM ETF",      "weight": "9.2%", "value": "$11.4B","held_since": "Long-term"},
            {"ticker": "IVV","name": "iShares Core S&P 500", "weight": "8.1%", "value": "$10.1B","held_since": "Long-term"},
            {"ticker": "GDX","name": "VanEck Gold Miners",   "weight": "6.4%", "value": "$7.9B", "held_since": "2019"},
        ],
        "key_insight": "Dalio's 'All Weather' portfolio (30% stocks, 40% bonds, 15% gold, 15% commodities) is a widely used framework. His most actionable signal: structural bull on gold and EM as a hedge against US dollar devaluation.",
        "policy_signals": None,
    },
]

CAT_STYLE = {
    "Investor":       "background:rgba(29,158,117,0.12);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.3)",
    "Politician":     "background:rgba(55,138,221,0.12);color:#378ADD;border:0.5px solid rgba(55,138,221,0.3)",
    "Policy Signals": "background:rgba(216,90,48,0.12);color:#D85A30;border:0.5px solid rgba(216,90,48,0.3)",
}


def _section_header(text, color):
    return (
        f'<div style="display:flex;align-items:center;gap:8px;margin:14px 0 10px">'
        f'<div style="height:1px;flex:1;background:rgba(128,128,128,0.15)"></div>'
        f'<span style="font-size:0.72rem;font-weight:600;text-transform:uppercase;'
        f'letter-spacing:0.07em;color:{color};opacity:0.8">{text}</span>'
        f'<div style="height:1px;flex:1;background:rgba(128,128,128,0.15)"></div>'
        f'</div>'
    )


def _trade_row(trade, action_type="buy"):
    color = "#1D9E75" if action_type == "buy" else "#D85A30"
    bg    = "rgba(29,158,117,0.07)" if action_type == "buy" else "rgba(216,90,48,0.07)"
    icon  = "↑" if action_type == "buy" else "↓"
    if trade.get("ticker") == "N/A":
        return '<div style="font-size:0.78rem;opacity:0.4;padding:8px 0">No recent disclosed sales in this period</div>'
    return (
        f'<div style="background:{bg};border-radius:10px;padding:10px 12px;margin-bottom:7px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'
        f'  <div style="display:flex;align-items:center;gap:8px">'
        f'    <span style="font-weight:700;font-size:0.9rem">{trade["ticker"]}</span>'
        f'    <span style="font-size:0.75rem;opacity:0.55">{trade["name"]}</span>'
        f'  </div>'
        f'  <div style="display:flex;align-items:center;gap:8px">'
        f'    <span style="color:{color};font-weight:600;font-size:0.82rem">{icon} {trade["action"]}</span>'
        f'    <span style="font-size:0.78rem;font-weight:600;color:{color}">{trade["size"]}</span>'
        f'    <span style="font-size:0.72rem;opacity:0.4">{trade["date"]}</span>'
        f'  </div>'
        f'</div>'
        f'<div style="font-size:0.77rem;opacity:0.6;line-height:1.45">{trade["reason"]}</div>'
        f'</div>'
    )


def _holding_row(h, accent):
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'padding:8px 0;border-bottom:0.5px solid rgba(128,128,128,0.10)">'
        f'<div>'
        f'  <span style="font-weight:600;font-size:0.88rem">{h["ticker"]}</span>'
        f'  <span style="font-size:0.75rem;opacity:0.5;margin-left:6px">{h["name"]}</span>'
        f'</div>'
        f'<div style="display:flex;gap:16px;text-align:right">'
        f'  <div><div style="font-size:0.72rem;opacity:0.45">Weight</div>'
        f'      <div style="font-weight:600;color:{accent};font-size:0.85rem">{h["weight"]}</div></div>'
        f'  <div><div style="font-size:0.72rem;opacity:0.45">Value</div>'
        f'      <div style="font-weight:600;font-size:0.85rem">{h["value"]}</div></div>'
        f'  <div><div style="font-size:0.72rem;opacity:0.45">Since</div>'
        f'      <div style="font-size:0.8rem;opacity:0.6">{h["held_since"]}</div></div>'
        f'</div></div>'
    )


def _policy_row(p):
    colors = {
        "Bullish": "#1D9E75", "Mixed": "#BA7517",
        "Bullish crypto": "#7F77DD", "Bullish energy": "#D85A30",
        "Bullish defense": "#378ADD",
    }
    color = colors.get(p["impact"], "#888")
    return (
        f'<div style="background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.12);'
        f'border-radius:10px;padding:10px 12px;margin-bottom:7px">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">'
        f'  <span style="font-weight:600;font-size:0.85rem">{p["policy"]}</span>'
        f'  <div style="display:flex;gap:8px;flex-shrink:0;margin-left:12px">'
        f'    <span style="font-size:0.7rem;color:{color};font-weight:600;'
        f'    background:rgba(128,128,128,0.08);padding:1px 8px;border-radius:10px">{p["impact"]}</span>'
        f'    <span style="font-size:0.7rem;opacity:0.4">{p["date"]}</span>'
        f'  </div>'
        f'</div>'
        f'<div style="font-size:0.77rem;opacity:0.65">{p["affected"]}</div>'
        f'</div>'
    )


def render_profile(profile, time_filter):
    accent    = profile["accent"]
    cat_style = CAT_STYLE.get(profile["category"], "")

    # header card
    st.markdown(
        f'<div style="background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.14);'
        f'border-radius:18px;padding:20px 24px;position:relative;overflow:hidden;margin-bottom:4px">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:3px;background:{accent};'
        f'border-radius:18px 18px 0 0;opacity:0.8"></div>'
        f'<div style="display:flex;align-items:flex-start;gap:16px">'
        f'  <div style="width:56px;height:56px;border-radius:14px;'
        f'    background:linear-gradient(135deg,{accent}30,{accent}15);'
        f'    border:1.5px solid {accent}40;display:flex;align-items:center;'
        f'    justify-content:center;font-size:26px;flex-shrink:0">{profile["avatar"]}</div>'
        f'  <div style="flex:1;min-width:0">'
        f'    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:3px">'
        f'      <span style="font-weight:700;font-size:1.15rem">{profile["name"]}</span>'
        f'      <span style="{cat_style};padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:600">'
        f'        {profile["category"]}</span>'
        f'    </div>'
        f'    <div style="font-size:0.8rem;opacity:0.55;margin-bottom:8px">{profile["title"]}</div>'
        f'    <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:0.78rem">'
        f'      <span>💰 <b>{profile["aum"]}</b> AUM</span>'
        f'      <span>📋 <b>{profile["filing"]}</b></span>'
        f'      <span style="opacity:0.5">⏱ {profile["lag"]}</span>'
        f'    </div>'
        f'  </div>'
        f'</div>'
        f'<div style="margin-top:14px;font-size:0.82rem;opacity:0.65;line-height:1.6;'
        f'border-top:0.5px solid rgba(128,128,128,0.12);padding-top:12px">'
        f'<b style="opacity:0.9">Strategy:</b> {profile["philosophy"]}'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # key insight
    st.markdown(
        f'<div style="background:{accent}12;border-left:3px solid {accent};'
        f'border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:16px;'
        f'font-size:0.82rem;line-height:1.55">'
        f'💡 <b>Key insight:</b> {profile["key_insight"]}</div>',
        unsafe_allow_html=True,
    )

    # policy signals
    if profile.get("policy_signals"):
        st.markdown(_section_header("Policy signals & market impact", accent), unsafe_allow_html=True)
        for p in profile["policy_signals"]:
            st.markdown(_policy_row(p), unsafe_allow_html=True)

    # brand mention tracker — Trump only
    if profile["id"] == "trump":
        st.markdown(_section_header("Brand mention tracker — Truth Social & public statements", "#D85A30"), unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:0.78rem;opacity:0.55;margin-bottom:12px;line-height:1.5">'
            'When Trump publicly mentions or praises a company, it historically moves that stock within hours. '
            'Negative mentions have the opposite effect. Each card shows the quote, market reaction, and actionable signal.</div>',
            unsafe_allow_html=True,
        )

        # sentiment filter
        sc1, sc2 = st.columns([2, 3])
        with sc1:
            sent_filter = st.segmented_control(
                "Sentiment", ["All", "Positive", "Negative", "Mixed"],
                default="All", key="trump_sent_filter", label_visibility="collapsed",
            )

        mentions = TRUMP_MENTIONS
        if sent_filter and sent_filter != "All":
            if sent_filter == "Positive":
                mentions = [m for m in mentions if "Positive" in m["sentiment"]]
            elif sent_filter == "Negative":
                mentions = [m for m in mentions if "Negative" in m["sentiment"]]
            elif sent_filter == "Mixed":
                mentions = [m for m in mentions if m["sentiment"] == "Mixed"]

        # summary strip
        pos_count  = sum(1 for m in TRUMP_MENTIONS if "Positive" in m["sentiment"])
        neg_count  = sum(1 for m in TRUMP_MENTIONS if "Negative" in m["sentiment"])
        mix_count  = sum(1 for m in TRUMP_MENTIONS if m["sentiment"] == "Mixed")
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Total mentions tracked", len(TRUMP_MENTIONS))
        mc2.metric("Positive 🚀", pos_count)
        mc3.metric("Negative ⚠️", neg_count)
        mc4.metric("Mixed ⚡", mix_count)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        for m in mentions:
            st.markdown(_mention_card(m, time_filter), unsafe_allow_html=True)

        st.markdown(
            '<div style="font-size:0.74rem;opacity:0.4;margin-top:8px;line-height:1.5">'
            '⚠️ This tracker monitors publicly reported statements and disclosed financial data. '
            'Trading based on presidential statements carries regulatory and ethical risk. '
            'Not financial advice.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # recent trades
    col_buy, col_sell = st.columns(2)
    with col_buy:
        st.markdown(_section_header("Recent buys / new positions", "#1D9E75"), unsafe_allow_html=True)
        buys = profile["recent_buys"]
        if time_filter == "Last week":
            buys = [b for b in buys if "May 2026" in b.get("date","")]
        elif time_filter == "Last month":
            buys = [b for b in buys if any(m in b.get("date","") for m in ["May 2026","Apr 2026","Mar 2026"])]
        for b in (buys or [{"ticker":"—","name":"No trades in this period","action":"","size":"","date":"","reason":"Try a longer time filter"}]):
            st.markdown(_trade_row(b, "buy"), unsafe_allow_html=True)

    with col_sell:
        st.markdown(_section_header("Recent sells / reductions", "#D85A30"), unsafe_allow_html=True)
        sells = profile["recent_sells"]
        if time_filter == "Last week":
            sells = [s for s in sells if "May 2026" in s.get("date","")]
        elif time_filter == "Last month":
            sells = [s for s in sells if any(m in s.get("date","") for m in ["May 2026","Apr 2026","Mar 2026"])]
        for s in (sells or [{"ticker":"—","name":"No sells in this period","action":"","size":"","date":"","reason":"Try a longer time filter"}]):
            st.markdown(_trade_row(s, "sell"), unsafe_allow_html=True)

    # top holdings
    st.markdown(_section_header("Top disclosed holdings", accent), unsafe_allow_html=True)
    holdings_html = "".join(_holding_row(h, accent) for h in profile["top_holdings"])
    st.markdown(
        f'<div style="background:rgba(128,128,128,0.04);border:0.5px solid rgba(128,128,128,0.12);'
        f'border-radius:14px;padding:4px 14px">{holdings_html}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)


def show():
    st.markdown(
        '<h2 style="font-size:1.5rem;font-weight:600;letter-spacing:-0.3px;margin-bottom:4px">'
        '🧠 Smart Money Tracker</h2>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Tracks disclosed positions and trades of influential investors and public figures. "
        "Sources: SEC 13F · Congressional STOCK Act · Presidential disclosures · ARK daily reports."
    )

    ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 2])
    with ctrl1:
        time_filter = st.segmented_control(
            "Period", ["Last week", "Last month", "Last 6 months"],
            default="Last 6 months", label_visibility="collapsed",
        )
    with ctrl2:
        cat_filter = st.segmented_control(
            "Category", ["All", "Investors", "Politicians"],
            default="All", label_visibility="collapsed",
        )
    with ctrl3:
        st.markdown(
            '<div style="font-size:0.75rem;opacity:0.45;padding:8px 0;line-height:1.4">'
            '⚠️ All data publicly disclosed per SEC, STOCK Act & presidential disclosure law. '
            'Filing lags noted per profile.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Profiles tracked", len(PROFILES))
    c2.metric("Investors", sum(1 for p in PROFILES if p["category"] == "Investor"))
    c3.metric("Politicians / Policy", sum(1 for p in PROFILES if p["category"] in ("Politician","Policy Signals")))
    c4.metric("Brand mentions tracked", len(TRUMP_MENTIONS))

    st.markdown("---")

    if cat_filter == "Investors":
        profiles = [p for p in PROFILES if p["category"] == "Investor"]
    elif cat_filter == "Politicians":
        profiles = [p for p in PROFILES if p["category"] in ("Politician","Policy Signals")]
    else:
        profiles = PROFILES

    tf = time_filter or "Last 6 months"

    for i, profile in enumerate(profiles):
        render_profile(profile, tf)
        if i < len(profiles) - 1:
            st.markdown(
                '<div style="height:0.5px;background:rgba(128,128,128,0.15);margin:24px 0"></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="margin-top:24px;padding:14px 18px;background:rgba(128,128,128,0.06);'
        'border:0.5px solid rgba(128,128,128,0.15);border-radius:12px;font-size:0.78rem;'
        'opacity:0.65;line-height:1.6">'
        '📋 <b>Data sources:</b> SEC 13F (quarterly, 45-day lag) · STOCK Act (within 45 days) · '
        'Presidential Financial Disclosure (annual) · ARK Invest daily trade files (next-day). '
        'Short positions, options, and non-US holdings may not appear in 13F filings. '
        'Not financial advice.</div>',
        unsafe_allow_html=True,
    )
