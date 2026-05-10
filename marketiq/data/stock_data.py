"""
Shared data used across all pages.
In production, replace static dicts with live API calls
(Yahoo Finance / NewsAPI / Alpha Vantage).
"""

# ── Stock universe with historical avg annual return ──────────────────────────
STOCKS = {
    "VOO":   {"name": "Vanguard S&P 500 ETF",   "rate": 0.107, "risk": "low"},
    "MSFT":  {"name": "Microsoft",               "rate": 0.175, "risk": "low"},
    "NVDA":  {"name": "Nvidia",                  "rate": 0.280, "risk": "high"},
    "GOOGL": {"name": "Alphabet",                "rate": 0.152, "risk": "mid"},
    "AMZN":  {"name": "Amazon",                  "rate": 0.165, "risk": "mid"},
    "META":  {"name": "Meta Platforms",          "rate": 0.210, "risk": "high"},
    "AVGO":  {"name": "Broadcom",                "rate": 0.220, "risk": "high"},
    "AAPL":  {"name": "Apple",                   "rate": 0.145, "risk": "low"},
    "BRK.B": {"name": "Berkshire Hathaway B",    "rate": 0.105, "risk": "low"},
    "NEE":   {"name": "NextEra Energy",          "rate": 0.118, "risk": "low"},
    "LMT":   {"name": "Lockheed Martin",         "rate": 0.112, "risk": "mid"},
    "EQIX":  {"name": "Equinix",                 "rate": 0.135, "risk": "mid"},
    "O":     {"name": "Realty Income",           "rate": 0.092, "risk": "low"},
    "GLD":   {"name": "SPDR Gold ETF",           "rate": 0.075, "risk": "low"},
    "XOM":   {"name": "ExxonMobil",              "rate": 0.095, "risk": "mid"},
    "AMAT":  {"name": "Applied Materials",       "rate": 0.195, "risk": "high"},
}

# ── Dashboard: buy & sell watchlists ─────────────────────────────────────────
TOP_BUYS = [
    {"ticker": "NVDA",  "name": "AI chips, data centers",    "price": 215.16, "chg": +1.8,  "signal": "Strong Buy"},
    {"ticker": "MSFT",  "name": "Cloud + AI leadership",     "price": 415.17, "chg": +1.3,  "signal": "Buy"},
    {"ticker": "AMZN",  "name": "AWS growth resuming",       "price": 272.66, "chg": +0.5,  "signal": "Buy"},
    {"ticker": "GOOGL", "name": "Search + Gemini AI",        "price": 170.50, "chg": +0.7,  "signal": "Buy"},
    {"ticker": "LLY",   "name": "GLP-1 drug pipeline",      "price": 841.00, "chg": +1.2,  "signal": "Buy"},
    {"ticker": "BRK.B", "name": "Defensive + value",         "price": 468.00, "chg": +0.4,  "signal": "Buy"},
    {"ticker": "AAPL",  "name": "Services moat growing",     "price": 293.41, "chg": +2.1,  "signal": "Buy"},
    {"ticker": "META",  "name": "Ad revenue + AI",           "price": 609.53, "chg": +0.6,  "signal": "Buy"},
    {"ticker": "NEE",   "name": "Clean energy + AI power",   "price": 73.20,  "chg": +0.5,  "signal": "Buy"},
    {"ticker": "VOO",   "name": "Your core holding",         "price": 678.10, "chg": +0.82, "signal": "Buy"},
]

TOP_SELLS = [
    {"ticker": "TSLA",  "name": "Valuation stretched post-rally",  "price": 427.99, "chg": +3.9,  "signal": "Reduce"},
    {"ticker": "INTC",  "name": "Lost AI chip war",                "price": 21.30,  "chg": -0.8,  "signal": "Avoid"},
    {"ticker": "DIS",   "name": "Streaming still unprofitable",    "price": 101.30, "chg": -0.5,  "signal": "Reduce"},
    {"ticker": "BABA",  "name": "Geopolitical + regulatory risk",  "price": 87.10,  "chg": -2.1,  "signal": "Avoid"},
    {"ticker": "CVS",   "name": "Insurance losses deepening",      "price": 53.00,  "chg": -1.2,  "signal": "Avoid"},
    {"ticker": "MPW",   "name": "Healthcare REIT distress",        "price": 4.00,   "chg": -3.1,  "signal": "Sell"},
    {"ticker": "PFE",   "name": "Post-COVID revenue cliff",        "price": 27.30,  "chg": -0.6,  "signal": "Reduce"},
    {"ticker": "WBA",   "name": "Pharmacy model under threat",     "price": 9.00,   "chg": -1.8,  "signal": "Sell"},
    {"ticker": "NIO",   "name": "EV competition crushing margins", "price": 3.50,   "chg": -2.4,  "signal": "Avoid"},
    {"ticker": "PARA",  "name": "Media disruption ongoing",        "price": 11.00,  "chg": -1.0,  "signal": "Sell"},
]

# ── News events with stock actions ───────────────────────────────────────────
NEWS_EVENTS = [
    {
        "type": "Risk",
        "category": "Trade War",
        "headline": "US-China trade tariffs escalate; tech supply chains under pressure",
        "logic": (
            "Hardware made in China becomes more expensive. Companies with China-dependent "
            "manufacturing get squeezed. But domestic US software and cloud businesses are "
            "immune — and even benefit as enterprises shift spending toward software efficiency tools."
        ),
        "actions": [
            {"ticker": "MSFT",  "action": "Buy",   "risk": "low",  "reason": "Pure software + cloud — zero China hardware dependency. Enterprises cut hardware, increase cloud spend.", "horizon": "3–5 yrs"},
            {"ticker": "GOOGL", "action": "Buy",   "risk": "low",  "reason": "Google Cloud and ad revenue unaffected by tariffs. TPU chips made in-house reduce supply chain risk.", "horizon": "3–5 yrs"},
            {"ticker": "AMAT",  "action": "Buy",   "risk": "mid",  "reason": "US tariffs accelerate domestic semiconductor fab buildout. AMAT supplies the equipment for those fabs.", "horizon": "2–4 yrs"},
            {"ticker": "AAPL",  "action": "Avoid", "risk": "high", "reason": "~90% of iPhones assembled in China. Tariffs directly compress margins or force price hikes.", "horizon": "Wait for clarity"},
        ],
    },
    {
        "type": "Opportunity",
        "category": "Monetary Policy",
        "headline": "Fed signals rate cuts may resume in H2 2026 if inflation cools",
        "logic": (
            "Lower interest rates reduce borrowing costs for high-growth companies. Growth stocks "
            "punished in the rate-hike cycle recover first. REITs and dividend stocks also rally "
            "because bonds become less attractive by comparison."
        ),
        "actions": [
            {"ticker": "AMZN", "action": "Buy",      "risk": "mid", "reason": "AWS capex-heavy expansion gets cheaper to finance. Growth multiple expands as rates fall.", "horizon": "3–5 yrs"},
            {"ticker": "META", "action": "Buy",      "risk": "mid", "reason": "Massive AI infrastructure investment benefits from lower borrowing costs.", "horizon": "2–4 yrs"},
            {"ticker": "O",    "action": "Buy",      "risk": "low", "reason": "REITs are direct rate-cut beneficiaries. Realty Income pays monthly dividends — 114 consecutive increases.", "horizon": "3–7 yrs"},
            {"ticker": "VOO",  "action": "Add more", "risk": "low", "reason": "Rate cuts are historically very bullish for the broad S&P 500. Increase your monthly DCA amount.", "horizon": "DCA monthly"},
        ],
    },
    {
        "type": "Opportunity",
        "category": "AI Infrastructure",
        "headline": "AI capex spending by hyperscalers hits record $250B globally",
        "logic": (
            "When Microsoft, Google, Amazon, and Meta spend $250B building AI infrastructure, "
            "that money flows to chip makers, data center builders, power companies, and cooling "
            "systems — the suppliers of the AI gold rush, not just the AI companies themselves."
        ),
        "actions": [
            {"ticker": "NVDA", "action": "Strong Buy", "risk": "high", "reason": "Every dollar of AI capex needs GPUs. NVDA has 80%+ market share in AI training chips.", "horizon": "3–5 yrs"},
            {"ticker": "AVGO", "action": "Buy",        "risk": "high", "reason": "Custom AI chips (ASICs) for Google and Meta. As hyperscalers diversify away from NVDA, AVGO wins.", "horizon": "3–5 yrs"},
            {"ticker": "NEE",  "action": "Buy",        "risk": "low",  "reason": "AI data centers consume massive power. NEE is the largest clean energy provider in the US.", "horizon": "5–10 yrs"},
            {"ticker": "EQIX", "action": "Buy",        "risk": "mid",  "reason": "World's largest data center REIT. Every AI model needs physical space — Equinix owns it globally.", "horizon": "5–10 yrs"},
        ],
    },
    {
        "type": "Risk",
        "category": "Geopolitical",
        "headline": "Middle East tensions weighing on oil prices and regional stability",
        "logic": (
            "Conflict in the Middle East disrupts oil supply routes, pushing crude prices higher. "
            "Higher oil = higher inflation globally, complicating Fed rate decisions. Creates "
            "opportunities in defense and energy stocks while hurting airlines and consumer discretionary."
        ),
        "actions": [
            {"ticker": "XOM",      "action": "Buy",   "risk": "mid",  "reason": "Higher oil prices directly boost ExxonMobil's profit margins. Strong balance sheet and dividend history.", "horizon": "During conflict"},
            {"ticker": "LMT",      "action": "Buy",   "risk": "low",  "reason": "Defense spending spikes during geopolitical crises. LMT is the world's largest defense contractor.", "horizon": "2–4 yrs"},
            {"ticker": "GLD",      "action": "Add",   "risk": "low",  "reason": "Gold is the ultimate safe haven during geopolitical uncertainty. Allocate 5–10% of portfolio.", "horizon": "As insurance"},
            {"ticker": "Airlines", "action": "Avoid", "risk": "high", "reason": "Airlines get crushed by rising fuel costs when oil spikes. Avoid until oil stabilizes below $80/barrel.", "horizon": "Stay away"},
        ],
    },
    {
        "type": "Watch",
        "category": "Macro",
        "headline": "Europe manufacturing PMI contracts for 8th consecutive month",
        "logic": (
            "Europe is in an industrial recession. This weakens the Euro, hurts European exporters, "
            "and drags on global growth. However, it accelerates capital flight into US assets — "
            "which is directly bullish for US large-cap stocks and your VOO position."
        ),
        "actions": [
            {"ticker": "VOO",  "action": "Keep DCA", "risk": "low",  "reason": "Global weakness drives capital into US assets. Your VOO position benefits directly — keep DCA running.", "horizon": "Continue monthly"},
            {"ticker": "BRK.B","action": "Buy",      "risk": "low",  "reason": "Domestic US business model with minimal Europe exposure. Buffett's cash lets him buy during global weakness.", "horizon": "3–5 yrs"},
            {"ticker": "VEA",  "action": "Avoid",    "risk": "high", "reason": "Direct exposure to contracting European markets. Avoid until PMI turns positive.", "horizon": "6–12 months"},
            {"ticker": "ASML", "action": "Hold only","risk": "mid",  "reason": "ASML's fundamentals are strong but European listing creates FX headwinds. Hold if owned, don't add.", "horizon": "Monitor quarterly"},
        ],
    },
]

# ── Mood profiles ─────────────────────────────────────────────────────────────
MOOD_PROFILES = {
    "Ambitious": {
        "emoji": "🔥",
        "description": "High-conviction growth and AI plays. Maximum upside, accepts volatility.",
        "expected": "18–35% annually",
        "horizon": "3–7 years",
        "volatility": "High — expect 20–40% drawdowns",
        "color": "#D85A30",
        "stocks": [
            {"ticker": "NVDA",  "pct": 30, "risk": "High",   "rationale": "Dominant AI chip maker. Highest upside in current cycle — pure conviction play."},
            {"ticker": "AVGO",  "pct": 20, "risk": "High",   "rationale": "Custom AI chip winner. Google & Meta depend on them. Explosive EPS growth."},
            {"ticker": "META",  "pct": 18, "risk": "High",   "rationale": "Ad revenue + AI monetization. Highest ROIC of the mega-caps right now."},
            {"ticker": "AMZN",  "pct": 15, "risk": "Medium", "rationale": "AWS reaccelerating. AI capex advantage. Rate cuts turbocharge the multiple."},
            {"ticker": "LMT",   "pct": 10, "risk": "Medium", "rationale": "Defense surge from Middle East tension. Backed by government contracts."},
            {"ticker": "AMAT",  "pct":  7, "risk": "High",   "rationale": "Tariff-driven domestic fab buildout. Every new chip factory needs AMAT equipment."},
        ],
    },
    "Cautious": {
        "emoji": "🛡️",
        "description": "Quality compounders and dividend payers. Sleep well, grow steadily.",
        "expected": "8–14% annually",
        "horizon": "5–10 years",
        "volatility": "Low — max expected drawdown ~12%",
        "color": "#1D9E75",
        "stocks": [
            {"ticker": "VOO",   "pct": 40, "risk": "Low",    "rationale": "Your core. Broadest diversification. Rate cuts are a direct tailwind. Keep DCA-ing."},
            {"ticker": "MSFT",  "pct": 20, "risk": "Low",    "rationale": "Safest mega-cap. Cloud moat, Copilot monetization, near-zero geopolitical risk."},
            {"ticker": "BRK.B", "pct": 15, "risk": "Low",    "rationale": "Buffett's $160B cash pile is a shield. Best defensive compounder in the market."},
            {"ticker": "O",     "pct": 12, "risk": "Low",    "rationale": "Monthly dividend, 114 consecutive increases. Rate cuts make this more attractive."},
            {"ticker": "GLD",   "pct":  8, "risk": "Low",    "rationale": "Hedge against Middle East tension and geopolitical uncertainty. Insurance position."},
            {"ticker": "NEE",   "pct":  5, "risk": "Low",    "rationale": "Largest clean energy provider. AI data center demand is accelerating its growth."},
        ],
    },
    "Curious": {
        "emoji": "🔭",
        "description": "Core stability with high-conviction satellite bets. Best of both worlds.",
        "expected": "12–22% annually",
        "horizon": "3–7 years",
        "volatility": "Medium — expect 10–20% drawdowns",
        "color": "#378ADD",
        "stocks": [
            {"ticker": "VOO",   "pct": 25, "risk": "Low",    "rationale": "Stable base. All rate-cut and AI tailwinds flow through here automatically."},
            {"ticker": "MSFT",  "pct": 18, "risk": "Low",    "rationale": "Quality growth anchor. Cloud + AI with lower volatility than pure-play AI names."},
            {"ticker": "NVDA",  "pct": 20, "risk": "High",   "rationale": "The boldest bet — supported by current AI spending data. Core conviction pick."},
            {"ticker": "GOOGL", "pct": 15, "risk": "Medium", "rationale": "Undervalued AI leader. Cheapest mega-cap on earnings basis. Solid floor with upside."},
            {"ticker": "XOM",   "pct": 12, "risk": "Medium", "rationale": "Middle East hedge. Benefits if oil stays elevated. Pays strong dividend while you wait."},
            {"ticker": "O",     "pct": 10, "risk": "Low",    "rationale": "Rate-cut beneficiary. Monthly income stream balances the volatility of growth picks."},
        ],
    },
}
