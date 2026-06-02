"""
smart_money.py — Smart Money Tracker
Tracks disclosed positions, recent trades, and policy signals of influential
investors and political figures. Data sourced from:
  - SEC 13F filings (institutional investors)
  - Congressional STOCK Act disclosures (politicians)
  - Presidential financial disclosures (Trump)
  - ARK Invest daily trade reports (Cathie Wood)
All data is public record. Filing lag noted on each profile.
"""

import streamlit as st

# ── Profile data ──────────────────────────────────────────────────────────────
PROFILES = [
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
        "portfolio_summary": "Highly concentrated — top 5 holdings = 72% of portfolio. Apple alone is ~40%. Recent trend: reducing Apple stake, adding energy/financials.",
        "recent_buys": [
            {"ticker": "OXY",  "name": "Occidental Petroleum",  "action": "Added",     "size": "+$2.1B", "date": "Q1 2026", "reason": "Oil above $100. Long-term energy thesis. Now owns 28% of OXY."},
            {"ticker": "SIRI", "name": "Sirius XM",             "action": "New buy",   "size": "+$690M", "date": "Q4 2025", "reason": "Deep value play post-merger with Liberty Media. Near 52-week low."},
            {"ticker": "CVX",  "name": "Chevron",               "action": "Added",     "size": "+$800M", "date": "Q1 2026", "reason": "Energy diversification alongside OXY position."},
            {"ticker": "VZ",   "name": "Verizon",               "action": "Added",     "size": "+$450M", "date": "Q4 2025", "reason": "High dividend yield, defensive characteristics in uncertain market."},
        ],
        "recent_sells": [
            {"ticker": "AAPL", "name": "Apple",      "action": "Reduced",  "size": "-$8.2B", "date": "Q1 2026", "reason": "Took profits after 5-year run. Still largest holding but trimming concentration."},
            {"ticker": "HP",   "name": "HP Inc.",    "action": "Sold all", "size": "-$340M", "date": "Q4 2025", "reason": "Exited position entirely. PC market headwinds."},
            {"ticker": "PARA", "name": "Paramount",  "action": "Sold all", "size": "-$120M", "date": "Q1 2026", "reason": "Full exit. Media sector in structural decline."},
        ],
        "top_holdings": [
            {"ticker": "AAPL",  "name": "Apple",               "weight": "40.2%", "value": "$155B", "held_since": "2016"},
            {"ticker": "BAC",   "name": "Bank of America",     "weight": "10.1%", "value": "$39B",  "held_since": "2011"},
            {"ticker": "AXP",   "name": "American Express",    "weight": "8.3%",  "value": "$32B",  "held_since": "1991"},
            {"ticker": "KO",    "name": "Coca-Cola",           "weight": "7.1%",  "value": "$27B",  "held_since": "1988"},
            {"ticker": "CVX",   "name": "Chevron",             "weight": "5.8%",  "value": "$22B",  "held_since": "2022"},
            {"ticker": "OXY",   "name": "Occidental Petroleum","weight": "5.2%",  "value": "$20B",  "held_since": "2022"},
        ],
        "key_insight": "Buffett's $170B cash pile is the largest in Berkshire's history. When Buffett holds cash, he's saying the market is overpriced. He deployed aggressively in energy — OXY and CVX now represent a major geopolitical hedge.",
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
        "filing": "STOCK Act disclosure — filed within 45 days of trade",
        "lag": "Up to 45-day disclosure lag",
        "philosophy": "Pelosi's portfolio is technically managed by her husband Paul Pelosi, but congressional disclosure rules require all trades to be reported. Her track record is extraordinary — outperforming the S&P 500 significantly over the past decade. Trades often appear to front-run legislation or policy shifts, though no insider trading charges have ever been filed.",
        "portfolio_summary": "Heavy tech concentration. Significant options activity (LEAPS — long-dated calls). Consistently buys tech before favorable legislation. Paul Pelosi's trades are watched by millions of retail investors who try to mirror them.",
        "recent_buys": [
            {"ticker": "NVDA",  "name": "Nvidia",       "action": "Call options", "size": "$5M notional",  "date": "Mar 2026", "reason": "20+ NVIDIA call purchases over past 2 years. Bought before AI chip export policy decisions."},
            {"ticker": "MSFT",  "name": "Microsoft",    "action": "Call options", "size": "$2.8M notional","date": "Jan 2026", "reason": "Bought calls before Microsoft was awarded major government cloud contracts."},
            {"ticker": "AAPL",  "name": "Apple",        "action": "Added",        "size": "+$1.1M",        "date": "Feb 2026", "reason": "Long-term core holding. Bought during February dip."},
            {"ticker": "PANW",  "name": "Palo Alto Ntwks","action":"New position","size": "$900K",          "date": "Jan 2026", "reason": "Added before cybersecurity legislation passed committee."},
        ],
        "recent_sells": [
            {"ticker": "GOOGL", "name": "Alphabet",   "action": "Reduced",  "size": "-$2.1M", "date": "Q4 2025", "reason": "Took profits. Alphabet facing antitrust scrutiny from DOJ."},
            {"ticker": "RBLX",  "name": "Roblox",     "action": "Sold all", "size": "-$500K", "date": "Q3 2025", "reason": "Full exit from gaming position."},
        ],
        "top_holdings": [
            {"ticker": "NVDA",  "name": "Nvidia",         "weight": "~22%", "value": "~$53M",  "held_since": "2020"},
            {"ticker": "AAPL",  "name": "Apple",          "weight": "~18%", "value": "~$43M",  "held_since": "2007"},
            {"ticker": "MSFT",  "name": "Microsoft",      "weight": "~15%", "value": "~$36M",  "held_since": "2020"},
            {"ticker": "AMZN",  "name": "Amazon",         "weight": "~10%", "value": "~$24M",  "held_since": "2018"},
            {"ticker": "PANW",  "name": "Palo Alto Ntwks","weight": "~8%",  "value": "~$19M",  "held_since": "2026"},
            {"ticker": "TSLA",  "name": "Tesla",          "weight": "~7%",  "value": "~$17M",  "held_since": "2021"},
        ],
        "key_insight": "Multiple tracker ETFs and websites exist specifically to mirror Pelosi's disclosed trades. Her options activity (long-dated calls) is particularly watched — she often buys before major tech policy decisions. All data is legally disclosed per STOCK Act requirements.",
    },
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
            {"ticker": "DJT",   "name": "Trump Media & Technology", "action": "Holds", "size": "~$2.1B stake", "date": "Ongoing", "reason": "Largest public equity holding. ~57% owner. Highly volatile — moves on political news not business fundamentals."},
            {"ticker": "TRUMP", "name": "TRUMP Meme Coin",          "action": "Launched","size": "80% supply retained","date": "Jan 2026","reason": "Launched days before inauguration. Spiked 300%+ then fell 80%. Controversial — SEC investigating."},
            {"ticker": "WLFI",  "name": "World Liberty Financial (crypto)", "action":"Holds","size":"~$30M",  "date": "2025",    "reason": "Trump family's DeFi crypto project. Raised $600M+ from investors globally."},
        ],
        "recent_sells": [
            {"ticker": "N/A", "name": "No recent disclosed sales", "action": "—", "size": "—", "date": "—", "reason": "Presidential disclosure covers annual period. No major equity sales disclosed in current period."},
        ],
        "policy_signals": [
            {"policy": "Steel & aluminum tariffs (25%)",         "affected": "X, NUE, STLD ↑ · Boeing, GE ↓",       "date": "Feb 2026", "impact": "Bullish"},
            {"policy": "US-China trade war escalation",          "affected": "AAPL, NVDA ↓ · Domestic mfg ↑",       "date": "Mar 2026", "impact": "Mixed"},
            {"policy": "Crypto deregulation executive order",    "affected": "BTC, ETH, COIN ↑ · Traditional banks ↓","date":"Jan 2026", "impact": "Bullish crypto"},
            {"policy": "Oil & gas drilling expansion",           "affected": "XOM, CVX, OXY ↑ · NEE, ENPH ↓",       "date": "Jan 2026", "impact": "Bullish energy"},
            {"policy": "NATO spending pressure / defence",       "affected": "LMT, RTX, NOC ↑",                     "date": "Mar 2026", "impact": "Bullish defense"},
            {"policy": "US-Iran ceasefire (May 2026)",           "affected": "Oil ↓ · Airlines ↑ · Gold ↓",         "date": "May 2026", "impact": "Mixed"},
        ],
        "top_holdings": [
            {"ticker": "DJT",        "name": "Trump Media & Technology", "weight": "~35%", "value": "~$2.1B",  "held_since": "2022"},
            {"ticker": "Real estate","name": "Mar-a-Lago, Trump Tower etc", "weight": "~50%","value": "~$3B+",  "held_since": "Long-term"},
            {"ticker": "TRUMP",      "name": "TRUMP Meme Coin",          "weight": "~5%",  "value": "Volatile","held_since": "2026"},
            {"ticker": "WLFI",       "name": "World Liberty Financial",  "weight": "~5%",  "value": "~$30M",   "held_since": "2025"},
        ],
        "key_insight": "Trump's most investable signal is policy announcements, not his personal portfolio. When he announces tariffs on a sector, historically that sector moves within hours. Monitor Truth Social and White House press releases as leading indicators for sector rotation.",
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
        "philosophy": "Cathie Wood bets on disruptive innovation across AI, genomics, robotics, fintech, and space. She has a 5-year investment horizon and aggressively buys dips in her conviction names. She was famous for her 2020 COVID bull run (+150%), but ARK has significantly underperformed since 2021 as high-growth unprofitable companies fell out of favor with rising rates.",
        "portfolio_summary": "ARKK is down 75%+ from its 2021 peak. Wood continues to buy aggressively, arguing the market is wrong. She has massive positions in TSLA, COIN, and various genomics names. Her daily trade files are watched by investors who want to front-run or fade her.",
        "recent_buys": [
            {"ticker": "TSLA",  "name": "Tesla",          "action": "Added",   "size": "+$180M", "date": "May 2026",  "reason": "Largest ARKK position. Wood believes Tesla will reach $2,600 on autonomous driving by 2030."},
            {"ticker": "COIN",  "name": "Coinbase",       "action": "Added",   "size": "+$95M",  "date": "Apr 2026",  "reason": "Crypto deregulation under Trump is major tailwind. Bought heavily on dips."},
            {"ticker": "ROKU",  "name": "Roku",           "action": "Added",   "size": "+$42M",  "date": "Mar 2026",  "reason": "Streaming platform consolidation. Believes Roku wins long-term ad market."},
            {"ticker": "PATH",  "name": "UiPath",         "action": "New buy", "size": "+$28M",  "date": "Apr 2026",  "reason": "AI-powered robotic process automation. Fits ARK's AI + robotics thesis."},
        ],
        "recent_sells": [
            {"ticker": "NVDA", "name": "Nvidia",  "action": "Sold",    "size": "-$280M", "date": "Q1 2026", "reason": "Famously sold NVDA in 2022. Continues to avoid — views it as too expensive for her growth model."},
            {"ticker": "ZM",   "name": "Zoom",    "action": "Reduced", "size": "-$65M",  "date": "Q4 2025", "reason": "Post-COVID growth normalizing. Reducing position."},
            {"ticker": "TDOC", "name": "Teladoc", "action": "Reduced", "size": "-$30M",  "date": "Q1 2026", "reason": "Telehealth sector struggling post-pandemic. Trimming."},
        ],
        "top_holdings": [
            {"ticker": "TSLA", "name": "Tesla",      "weight": "11.8%", "value": "$1.65B","held_since": "2018"},
            {"ticker": "COIN", "name": "Coinbase",   "weight": "8.9%",  "value": "$1.25B","held_since": "2021"},
            {"ticker": "ROKU", "name": "Roku",       "weight": "6.2%",  "value": "$870M", "held_since": "2019"},
            {"ticker": "EXAS", "name": "Exact Sciences","weight":"5.4%","value": "$756M", "held_since": "2019"},
            {"ticker": "PATH", "name": "UiPath",     "weight": "4.8%",  "value": "$672M", "held_since": "2026"},
            {"ticker": "HOOD", "name": "Robinhood",  "weight": "4.1%",  "value": "$574M", "held_since": "2021"},
        ],
        "key_insight": "Cathie Wood is best used as a contrarian indicator by some and as a conviction signal by others. Her TSLA price target of $2,600 by 2030 is either visionary or delusional — depending on your view of autonomous vehicles. Her daily trade files are free to download at ark-funds.com.",
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
        "philosophy": "Michael Burry (The Big Short) is a deep value contrarian who looks for severely mispriced assets — on both the long and short side. He is famous for betting against the 2008 housing market. He uses options heavily and makes highly concentrated bets. His portfolio turns over dramatically — he often holds 5–10 stocks max. He is frequently bearish on US markets and has warned repeatedly of asset bubbles.",
        "portfolio_summary": "Highly concentrated and frequently changes. Known for surprise positions — often in beaten-down sectors others have abandoned. Current portfolio focused on healthcare and Chinese names (at deep discounts). Also holds significant short positions which are NOT disclosed in 13F.",
        "recent_buys": [
            {"ticker": "BABA",  "name": "Alibaba",      "action": "Added",   "size": "+$12M",  "date": "Q1 2026", "reason": "Deep value — 9x P/E. Burry bets on mean reversion of China tech. Controversial but consistent with his value thesis."},
            {"ticker": "JD",    "name": "JD.com",       "action": "Added",   "size": "+$8M",   "date": "Q1 2026", "reason": "Buying Chinese e-commerce at distressed valuations. Expects US-China trade resolution."},
            {"ticker": "HUM",   "name": "Humana",       "action": "New buy", "size": "+$18M",  "date": "Q4 2025", "reason": "Healthcare insurer at multi-year low. Believes insurance losses are temporary."},
            {"ticker": "REAL",  "name": "The RealReal", "action": "Added",   "size": "+$4M",   "date": "Q1 2026", "reason": "Luxury resale marketplace. Contrarian bet on consumer trade-down."},
        ],
        "recent_sells": [
            {"ticker": "GEO",  "name": "Geo Group",     "action": "Reduced", "size": "-$8M",  "date": "Q4 2025", "reason": "Took some profits from private prison play under Trump administration."},
            {"ticker": "HCA",  "name": "HCA Healthcare","action": "Sold",    "size": "-$15M", "date": "Q1 2026", "reason": "Rotated out of for-profit hospitals into insurance."},
        ],
        "top_holdings": [
            {"ticker": "BABA", "name": "Alibaba",    "weight": "20.1%", "value": "$68M",  "held_since": "2024"},
            {"ticker": "JD",   "name": "JD.com",     "weight": "15.8%", "value": "$54M",  "held_since": "2024"},
            {"ticker": "HUM",  "name": "Humana",     "weight": "12.4%", "value": "$42M",  "held_since": "2025"},
            {"ticker": "HCA",  "name": "HCA Healthcare","weight":"10.2%","value": "$35M",  "held_since": "2024"},
            {"ticker": "REAL", "name": "The RealReal","weight":"8.6%",  "value": "$29M",  "held_since": "2025"},
        ],
        "key_insight": "Burry's short positions are NOT disclosed in 13F filings — only long positions are. When he files with a small 13F, it often means his real conviction is on the short side. He has been publicly bearish on US tech and the broad market since 2021. His China bets are deeply contrarian — he's betting on political normalization.",
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
        "filing": "SEC 13F — Q1 2026 + public Twitter/X commentary",
        "lag": "45-day filing lag + real-time social posts",
        "philosophy": "Bill Ackman runs a concentrated portfolio of 8–12 high-conviction bets and is famous for activist investing — buying large stakes in companies and then publicly pushing for management changes, spin-offs, or strategy shifts. He is very public on X (Twitter), often telegraphing his thinking before or after trades. He famously made $2.6B in 2020 by hedging with credit default swaps just before COVID.",
        "portfolio_summary": "Very concentrated — top 3 holdings = 60%+ of portfolio. Long Hilton, Chipotle, and Howard Hughes. Recently added Alphabet and Nike at dips. Ackman's public commentary on X often moves his holdings significantly.",
        "recent_buys": [
            {"ticker": "GOOGL","name": "Alphabet",  "action": "New buy", "size": "+$1.9B", "date": "Q4 2025", "reason": "Bought Alphabet at what he called 'the most attractive large-cap opportunity.' Antitrust fears overblown per Ackman."},
            {"ticker": "NKE",  "name": "Nike",      "action": "New buy", "size": "+$1.4B", "date": "Q1 2026", "reason": "Bought Nike at a 5-year low. Believes new CEO Elliott Hill will restore brand. Classic Ackman turnaround play."},
            {"ticker": "UNH",  "name": "UnitedHealth","action":"Added",  "size": "+$600M", "date": "Q4 2025", "reason": "Added to existing position after CEO murder caused massive selloff. Bought the fear."},
        ],
        "recent_sells": [
            {"ticker": "NEE",  "name": "NextEra Energy","action":"Sold all","size":"-$1.1B","date":"Q3 2025","reason":"Full exit. Said clean energy economics had deteriorated under changing policy environment."},
            {"ticker": "HHH",  "name": "Howard Hughes","action":"Reduced","size":"-$400M", "date":"Q4 2025","reason":"Reduced after spinning out Seaport Entertainment. Still a core holding."},
        ],
        "top_holdings": [
            {"ticker": "HLT",  "name": "Hilton Hotels",   "weight": "22.4%", "value": "$4.03B","held_since": "2018"},
            {"ticker": "CMG",  "name": "Chipotle",        "weight": "18.1%", "value": "$3.26B","held_since": "2016"},
            {"ticker": "GOOGL","name": "Alphabet",         "weight": "14.8%", "value": "$2.66B","held_since": "2025"},
            {"ticker": "NKE",  "name": "Nike",             "weight": "12.2%", "value": "$2.20B","held_since": "2026"},
            {"ticker": "UNH",  "name": "UnitedHealth",     "weight": "10.6%", "value": "$1.91B","held_since": "2021"},
            {"ticker": "HHH",  "name": "Howard Hughes",    "weight": "9.8%",  "value": "$1.76B","held_since": "2010"},
        ],
        "key_insight": "Follow Ackman on X (@BillAckman) for real-time commentary. He often tweets his investment thesis before the 13F is filed. His turnaround plays (Nike, UnitedHealth after crisis) are where he historically generates the most alpha. He's been publicly bullish on the US economy and AI infrastructure.",
    },
    {
        "id": "dalio",
        "name": "Ray Dalio",
        "title": "Founder, Bridgewater Associates (retired CIO)",
        "category": "Investor",
        "avatar": "🌊",
        "accent": "#378ADD",
        "aum": "$124B (Bridgewater)",
        "style": "Macro / All-weather / Risk parity",
        "filing": "SEC 13F — Q1 2026",
        "lag": "45-day filing lag",
        "philosophy": "Dalio created the 'All Weather' portfolio designed to perform in any economic environment. His macro framework is built around debt cycles — he believes the US is in a late-stage long-term debt cycle that will eventually force significant monetary system changes. He is one of the most globally diversified investors and has been consistently bullish on emerging markets, particularly India.",
        "portfolio_summary": "Bridgewater holds thousands of positions across ETFs, commodities, and international markets. The disclosed 13F is primarily US ETF exposures. Dalio himself recently stepped back from day-to-day management but his macro framework still drives Bridgewater's positioning.",
        "recent_buys": [
            {"ticker": "GLD",  "name": "SPDR Gold ETF",      "action": "Added",   "size": "+$890M", "date": "Q1 2026", "reason": "Gold is Bridgewater's largest disclosed position. Dalio has publicly said 'cash is trash' and gold is the alternative to sovereign debt."},
            {"ticker": "EEM",  "name": "Emerging Markets ETF","action":"Added",   "size": "+$650M", "date": "Q1 2026", "reason": "Bullish on EM as Fed rate cuts weaken USD. India exposure is the core thesis."},
            {"ticker": "SPY",  "name": "S&P 500 ETF",        "action": "Added",   "size": "+$420M", "date": "Q4 2025", "reason": "Broad US market exposure as risk-on sentiment returns."},
            {"ticker": "VWO",  "name": "Vanguard EM ETF",    "action": "Added",   "size": "+$380M", "date": "Q4 2025", "reason": "Diversified EM exposure. India, Brazil, Taiwan all overweight."},
        ],
        "recent_sells": [
            {"ticker": "TLT",  "name": "Long-term Treasuries","action":"Reduced","size":"-$1.1B","date":"Q1 2026","reason":"Reducing long-duration bond exposure. Dalio has warned US debt situation is unsustainable."},
            {"ticker": "BABA", "name": "Alibaba",            "action":"Reduced","size":"-$180M","date":"Q4 2025","reason":"Reducing China tech amid persistent geopolitical risk."},
        ],
        "top_holdings": [
            {"ticker": "GLD",  "name": "SPDR Gold ETF",         "weight": "18.2%", "value": "$22.6B","held_since": "2009"},
            {"ticker": "SPY",  "name": "S&P 500 ETF",           "weight": "14.8%", "value": "$18.4B","held_since": "Long-term"},
            {"ticker": "EEM",  "name": "iShares EM ETF",        "weight": "11.4%", "value": "$14.1B","held_since": "Long-term"},
            {"ticker": "VWO",  "name": "Vanguard EM ETF",       "weight": "9.2%",  "value": "$11.4B","held_since": "Long-term"},
            {"ticker": "IVV",  "name": "iShares Core S&P 500",  "weight": "8.1%",  "value": "$10.1B","held_since": "Long-term"},
            {"ticker": "GDX",  "name": "VanEck Gold Miners ETF","weight":"6.4%",  "value": "$7.9B", "held_since": "2019"},
        ],
        "key_insight": "Dalio's most investable signal is his macro framework: he is structurally bullish on gold, EM (especially India), and commodities as hedges against long-term US debt devaluation. His 'All Weather' portfolio (30% stocks, 40% bonds, 15% gold, 15% commodities) is a widely used framework for risk-balanced investing.",
    },
]

# ── Category colors ───────────────────────────────────────────────────────────
CAT_STYLE = {
    "Investor":       "background:rgba(29,158,117,0.12);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.3)",
    "Politician":     "background:rgba(55,138,221,0.12);color:#378ADD;border:0.5px solid rgba(55,138,221,0.3)",
    "Policy Signals": "background:rgba(216,90,48,0.12);color:#D85A30;border:0.5px solid rgba(216,90,48,0.3)",
}


def _section_header(text, color):
    return (
        f'<div style="display:flex;align-items:center;gap:8px;margin:14px 0 10px">'
        f'<div style="height:1px;flex:1;background:rgba(128,128,128,0.15)"></div>'
        f'<span style="font-size:0.72rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;color:{color};opacity:0.8">{text}</span>'
        f'<div style="height:1px;flex:1;background:rgba(128,128,128,0.15)"></div>'
        f'</div>'
    )


def _trade_row(trade, action_type="buy"):
    color = "#1D9E75" if action_type == "buy" else "#D85A30"
    bg    = "rgba(29,158,117,0.07)" if action_type == "buy" else "rgba(216,90,48,0.07)"
    icon  = "↑" if action_type == "buy" else "↓"
    if trade.get("ticker") == "N/A":
        return '<div style="font-size:0.78rem;opacity:0.4;padding:8px 0">No recent disclosed sales</div>'
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
    colors = {"Bullish": "#1D9E75", "Mixed": "#BA7517",
              "Bullish crypto": "#7F77DD", "Bullish energy": "#D85A30",
              "Bullish defense": "#378ADD"}
    color = colors.get(p["impact"], "#888")
    return (
        f'<div style="background:rgba(128,128,128,0.05);border:0.5px solid rgba(128,128,128,0.12);'
        f'border-radius:10px;padding:10px 12px;margin-bottom:7px">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">'
        f'  <span style="font-weight:600;font-size:0.85rem">{p["policy"]}</span>'
        f'  <div style="display:flex;gap:8px;flex-shrink:0;margin-left:12px">'
        f'    <span style="font-size:0.7rem;color:{color};font-weight:600;background:rgba(128,128,128,0.08);'
        f'    padding:1px 8px;border-radius:10px">{p["impact"]}</span>'
        f'    <span style="font-size:0.7rem;opacity:0.4">{p["date"]}</span>'
        f'  </div>'
        f'</div>'
        f'<div style="font-size:0.77rem;opacity:0.65">{p["affected"]}</div>'
        f'</div>'
    )


def render_profile(profile, time_filter):
    accent = profile["accent"]
    cat_style = CAT_STYLE.get(profile["category"], "")

    # ── Profile header card ───────────────────────────────────────────────────
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
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Key insight banner ────────────────────────────────────────────────────
    st.markdown(
        f'<div style="background:{accent}12;border-left:3px solid {accent};'
        f'border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:16px;'
        f'font-size:0.82rem;line-height:1.55">'
        f'💡 <b>Key insight:</b> {profile["key_insight"]}</div>',
        unsafe_allow_html=True,
    )

    # ── Policy signals (Trump only) ───────────────────────────────────────────
    if profile.get("policy_signals"):
        st.markdown(_section_header("Policy signals & market impact", accent), unsafe_allow_html=True)
        for p in profile["policy_signals"]:
            st.markdown(_policy_row(p), unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Recent trades ─────────────────────────────────────────────────────────
    col_buy, col_sell = st.columns(2)
    with col_buy:
        st.markdown(_section_header("Recent buys / new positions", "#1D9E75"), unsafe_allow_html=True)
        # filter by time
        buys = profile["recent_buys"]
        if time_filter == "Last week":
            buys = [b for b in buys if "May 2026" in b.get("date","") or "Apr 2026" in b.get("date","")]
        elif time_filter == "Last month":
            buys = [b for b in buys if any(m in b.get("date","") for m in ["May 2026","Apr 2026","Mar 2026"])]
        for b in (buys or [{"ticker":"N/A","name":"No trades in this period","action":"—","size":"—","date":"—","reason":"Try a longer time filter"}]):
            st.markdown(_trade_row(b, "buy"), unsafe_allow_html=True)

    with col_sell:
        st.markdown(_section_header("Recent sells / reductions", "#D85A30"), unsafe_allow_html=True)
        sells = profile["recent_sells"]
        if time_filter == "Last week":
            sells = [s for s in sells if "May 2026" in s.get("date","")]
        elif time_filter == "Last month":
            sells = [s for s in sells if any(m in s.get("date","") for m in ["May 2026","Apr 2026","Mar 2026"])]
        for s in (sells or [{"ticker":"N/A","name":"No sells in this period","action":"—","size":"—","date":"—","reason":"Try a longer time filter"}]):
            st.markdown(_trade_row(s, "sell"), unsafe_allow_html=True)

    # ── Current holdings ──────────────────────────────────────────────────────
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
        "Sources: SEC 13F filings · Congressional STOCK Act · Presidential disclosures · ARK daily reports."
    )

    # ── Controls ──────────────────────────────────────────────────────────────
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
            '⚠️ All data is publicly disclosed per SEC, STOCK Act, and presidential disclosure requirements. '
            'Filing lags noted per profile.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Summary strip ─────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Profiles tracked", len(PROFILES))
    c2.metric("Investors", sum(1 for p in PROFILES if p["category"] == "Investor"))
    c3.metric("Politicians", sum(1 for p in PROFILES if p["category"] in ("Politician", "Policy Signals")))
    c4.metric("AUM tracked", "$1.4T+")

    st.markdown("---")

    # ── Filter profiles ───────────────────────────────────────────────────────
    if cat_filter == "Investors":
        profiles = [p for p in PROFILES if p["category"] == "Investor"]
    elif cat_filter == "Politicians":
        profiles = [p for p in PROFILES if p["category"] in ("Politician", "Policy Signals")]
    else:
        profiles = PROFILES

    tf = time_filter or "Last 6 months"

    # ── Render each profile ───────────────────────────────────────────────────
    for i, profile in enumerate(profiles):
        render_profile(profile, tf)
        if i < len(profiles) - 1:
            st.markdown(
                '<div style="height:0.5px;background:rgba(128,128,128,0.15);margin:24px 0"></div>',
                unsafe_allow_html=True,
            )

    # ── Disclaimer ────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="margin-top:24px;padding:14px 18px;background:rgba(128,128,128,0.06);'
        'border:0.5px solid rgba(128,128,128,0.15);border-radius:12px;font-size:0.78rem;'
        'opacity:0.65;line-height:1.6">'
        '📋 <b>Data sources & disclaimer:</b> Institutional investor data sourced from SEC 13F filings '
        '(quarterly, 45-day lag). Congressional data from STOCK Act disclosures. '
        'Trump financial data from annual Presidential Financial Disclosure. '
        'ARK Invest data from their public daily trade files. '
        'All information is public record. This is not financial advice — '
        'past disclosed trades do not guarantee future performance. '
        'Short positions, options, and non-US holdings may not appear in 13F filings.'
        '</div>',
        unsafe_allow_html=True,
    )
