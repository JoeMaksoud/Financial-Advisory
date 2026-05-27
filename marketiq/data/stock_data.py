"""
stock_data.py — Market data, ETF & stock recommendations with full fundamentals.
Prices as of May 2026. Live prices override these via yfinance when deployed.
"""

# ── ETF Buy recommendations ───────────────────────────────────────────────────
ETF_BUYS = [
    {
        "ticker": "VOO", "name": "Vanguard S&P 500", "price": 678.10, "chg": +0.82,
        "signal": "Strong Buy", "score": 94,
        "thesis": "Broadest US large-cap exposure. S&P at all-time highs driven by AI earnings boom. Best long-term DCA vehicle. 10.7% avg annual return over 20 years.",
        "factors": {"Revenue trend": "↑", "Macro": "↑", "Momentum": "↑", "Risk": "Low"},
    },
    {
        "ticker": "QQQM", "name": "Invesco Nasdaq-100 Mini", "price": 198.40, "chg": +1.3,
        "signal": "Buy", "score": 88,
        "thesis": "Lower-cost QQQ. Concentrated in top AI/tech names. Outperforms S&P in bull cycles. AI capex boom directly benefits top 10 holdings.",
        "factors": {"Revenue trend": "↑", "Macro": "↑", "Momentum": "↑", "Risk": "Mid"},
    },
    {
        "ticker": "SOXX", "name": "iShares Semiconductor", "price": 212.30, "chg": +2.1,
        "signal": "Buy", "score": 87,
        "thesis": "AI chip demand is structural. Holds NVDA, AMD, AVGO, TSM, AMAT. Semiconductor revenue growing 35% YoY on average across holdings.",
        "factors": {"Revenue trend": "↑↑", "Macro": "↑", "Momentum": "↑", "Risk": "Mid"},
    },
    {
        "ticker": "ITA", "name": "iShares Aerospace & Defense", "price": 148.60, "chg": +0.9,
        "signal": "Buy", "score": 85,
        "thesis": "Middle East conflict + NATO at record spending. Defense budgets locked in 5+ years. LMT, RTX, NOC, GD all held. Non-cyclical government contracts.",
        "factors": {"Revenue trend": "↑", "Macro": "↑↑", "Momentum": "↑", "Risk": "Low"},
    },
    {
        "ticker": "SCHD", "name": "Schwab US Dividend Equity", "price": 28.40, "chg": +0.3,
        "signal": "Buy", "score": 82,
        "thesis": "High-quality dividend growers. 3.5% yield. Defensive for uncertain macro. Outperforms in rate-cut environments. Quality screen removes weak companies.",
        "factors": {"Revenue trend": "↑", "Macro": "↑", "Momentum": "→", "Risk": "Low"},
    },
    {
        "ticker": "VGK", "name": "Vanguard European ETF", "price": 74.20, "chg": +0.4,
        "signal": "Accumulate", "score": 72,
        "thesis": "Europe PMI turning after 8-month contraction. ECB cutting rates faster than Fed. Trades at 30% discount to US on P/E. Currency tailwind if EUR strengthens.",
        "factors": {"Revenue trend": "→", "Macro": "↑", "Momentum": "→", "Risk": "Mid"},
    },
    {
        "ticker": "EWJ", "name": "iShares MSCI Japan", "price": 72.10, "chg": +0.5,
        "signal": "Accumulate", "score": 70,
        "thesis": "Japan corporate governance reforms unlocking shareholder value. BOJ policy shift tailwind. Cheap vs global peers. Buffett has been buying Japanese stocks publicly.",
        "factors": {"Revenue trend": "↑", "Macro": "↑", "Momentum": "↑", "Risk": "Mid"},
    },
    {
        "ticker": "VWO", "name": "Vanguard Emerging Markets", "price": 44.80, "chg": +0.6,
        "signal": "Watch", "score": 68,
        "thesis": "India and SE Asia fastest growing EM economies. Fed rate cuts weaken USD → boosts EM. Long-term diversifier. 5-10 year horizon.",
        "factors": {"Revenue trend": "↑", "Macro": "→", "Momentum": "→", "Risk": "High"},
    },
]

# ── ETF Sell / Avoid ──────────────────────────────────────────────────────────
ETF_SELLS = [
    {
        "ticker": "VNQ", "name": "Vanguard Real Estate", "price": 82.30, "chg": -0.5,
        "signal": "Avoid", "score": 28,
        "thesis": "Commercial real estate under pressure from hybrid work + high financing costs. Rates still too high for REITs to refinance profitably.",
        "factors": {"Revenue trend": "↓", "Macro": "↓", "Momentum": "↓", "Risk": "High"},
    },
    {
        "ticker": "ARKK", "name": "ARK Innovation ETF", "price": 48.20, "chg": -1.2,
        "signal": "Avoid", "score": 22,
        "thesis": "80%+ down from peak. Portfolio of unprofitable speculative companies. No near-term earnings path. Better innovation exposure via SOXX or QQQ.",
        "factors": {"Revenue trend": "↓", "Macro": "↓", "Momentum": "↓", "Risk": "Very High"},
    },
    {
        "ticker": "TLT", "name": "iShares 20Y+ Treasury", "price": 88.20, "chg": -0.4,
        "signal": "Reduce", "score": 32,
        "thesis": "Long-duration bonds face headwinds. Inflation sticky at 3.2%. Fed not cutting until H2 2026. Don't over-allocate to long bonds yet.",
        "factors": {"Revenue trend": "↓", "Macro": "↓", "Momentum": "↓", "Risk": "Mid"},
    },
    {
        "ticker": "XLE", "name": "SPDR Energy Select", "price": 88.40, "chg": -0.8,
        "signal": "Reduce", "score": 38,
        "thesis": "Oil above $100 unsustainable long-term. US-Iran ceasefire could collapse oil 20%+ rapidly. Trim energy ETF exposure now while elevated.",
        "factors": {"Revenue trend": "→", "Macro": "↓", "Momentum": "→", "Risk": "High"},
    },
    {
        "ticker": "GLD", "name": "SPDR Gold ETF", "price": 310.20, "chg": -0.2,
        "signal": "Trim", "score": 45,
        "thesis": "Gold had a massive run on geopolitical fears. Ceasefire holding → gold faces correction. Trim to 5% max portfolio weight. Don't chase.",
        "factors": {"Revenue trend": "→", "Macro": "→", "Momentum": "↓", "Risk": "Mid"},
    },
]

# ── Stock Buy recommendations — fundamentals-first ────────────────────────────
STOCK_BUYS = [
    {
        "ticker": "NVDA", "name": "Nvidia", "region": "🇺🇸 US", "sector": "Semiconductors",
        "price": 215.16, "chg": +1.8, "signal": "Strong Buy", "score": 96,
        "fundamentals": {
            "Revenue growth (YoY)": "+122%",
            "Forward P/E": "28x (sector avg 35x — cheap)",
            "Analyst consensus": "94% Buy — 47 analysts",
            "12M price target": "$280 avg → +30% upside",
            "EPS growth": "+140% YoY",
            "Free cash flow": "$27B trailing",
            "Short interest": "1.2% — minimal",
        },
        "thesis": "Revenue +122% YoY. Forward P/E is actually below sector average despite dominant market position. 94% analyst Buy rate. AI hyperscaler capex is a multi-year structural demand. Blackwell GPU cycle just beginning. $280 price target implies 30% upside from today.",
        "risks": "Valuation sensitive to AI spending slowdown. China export restrictions.",
        "horizon": "3–5 years",
    },
    {
        "ticker": "ASML", "name": "ASML Holding", "region": "🇳🇱 Netherlands", "sector": "Chip Equipment",
        "price": 680.00, "chg": +0.7, "signal": "Buy", "score": 89,
        "fundamentals": {
            "Revenue growth (YoY)": "+24%",
            "Forward P/E": "32x",
            "Analyst consensus": "85% Buy — 28 analysts",
            "12M price target": "$850 avg → +25% upside",
            "EPS growth": "+28% YoY",
            "Free cash flow": "$8B trailing",
            "Backlog": "€36B — 2 years locked in",
        },
        "thesis": "Only company on earth that makes EUV lithography machines. Every advanced chip (Apple, NVDA, AMD) is impossible without them. €36B backlog = 2 years of revenue already secured. Non-US exposure adds portfolio diversification. Monopoly moat.",
        "risks": "China export restrictions limiting a key market.",
        "horizon": "5–10 years",
    },
    {
        "ticker": "APP", "name": "AppLovin", "region": "🇺🇸 US", "sector": "AI / Ad Tech",
        "price": 312.40, "chg": +2.4, "signal": "Buy", "score": 87,
        "fundamentals": {
            "Revenue growth (YoY)": "+44%",
            "Forward P/E": "38x",
            "Analyst consensus": "80% Buy — 22 analysts",
            "12M price target": "$420 avg → +34% upside",
            "EPS growth": "+180% YoY",
            "Free cash flow": "$4.2B, 35% margin",
            "Short interest": "4.1%",
        },
        "thesis": "One of the fastest growing AI companies most investors overlook. Ad tech using proprietary AI to optimize mobile advertising. EPS +180% YoY. Free cash flow margin of 35%. Under-the-radar vs Mag 7 but outperforming most of them on growth.",
        "risks": "Gaming sector exposure. High short interest creates volatility.",
        "horizon": "2–4 years",
    },
    {
        "ticker": "SAP", "name": "SAP SE", "region": "🇩🇪 Germany", "sector": "Enterprise Software",
        "price": 242.80, "chg": +0.5, "signal": "Buy", "score": 83,
        "fundamentals": {
            "Revenue growth (YoY)": "+11%",
            "Forward P/E": "35x",
            "Analyst consensus": "78% Buy — 32 analysts",
            "12M price target": "$290 avg → +19% upside",
            "EPS growth": "+18% YoY",
            "Free cash flow": "$7.1B trailing",
            "Cloud revenue growth": "+30% YoY",
        },
        "thesis": "SAP runs financial systems of 80% of Fortune 500 companies. Cloud transition accelerating — cloud now 40% of revenue growing 30% YoY. Non-US large-cap with recession-resistant enterprise contracts. Underappreciated AI play via Joule assistant.",
        "risks": "Slow enterprise sales cycles. EUR/USD FX exposure.",
        "horizon": "3–5 years",
    },
    {
        "ticker": "MELI", "name": "MercadoLibre", "region": "🇧🇷 LatAm", "sector": "E-commerce / Fintech",
        "price": 2100.00, "chg": +1.1, "signal": "Buy", "score": 85,
        "fundamentals": {
            "Revenue growth (YoY)": "+37%",
            "Forward P/E": "42x",
            "Analyst consensus": "82% Buy — 26 analysts",
            "12M price target": "$2,600 avg → +24% upside",
            "EPS growth": "+58% YoY",
            "Active users": "220M across 18 countries",
            "Free cash flow": "$3.8B trailing",
        },
        "thesis": "Amazon + PayPal of Latin America combined. 220M active users. Fintech arm (Mercado Pago) growing faster than marketplace. LatAm middle class expanding rapidly. Digital commerce penetration still low — long runway ahead.",
        "risks": "FX risk in Argentina/Brazil. Regulatory exposure.",
        "horizon": "5–10 years",
    },
    {
        "ticker": "MSFT", "name": "Microsoft", "region": "🇺🇸 US", "sector": "Cloud / AI",
        "price": 415.17, "chg": +1.3, "signal": "Buy", "score": 91,
        "fundamentals": {
            "Revenue growth (YoY)": "+17%",
            "Forward P/E": "30x (sector avg 35x)",
            "Analyst consensus": "92% Buy — 50 analysts",
            "12M price target": "$510 avg → +23% upside",
            "EPS growth": "+22% YoY",
            "Free cash flow": "$75B trailing",
            "Azure growth": "+35% QoQ",
        },
        "thesis": "Azure cloud growing 35%. Copilot AI monetizing across 400M Office users. $75B FCF gives defensive floor. 92% analyst Buy rate. Most analysts target $510+. Only mega-cap with AI embedded across every product line — not just one division.",
        "risks": "Antitrust scrutiny. AI investment not yet fully monetized at scale.",
        "horizon": "3–5 years",
    },
    {
        "ticker": "SE", "name": "Sea Limited", "region": "🇸🇬 Singapore", "sector": "SE Asia Digital",
        "price": 112.40, "chg": +0.9, "signal": "Watch", "score": 71,
        "fundamentals": {
            "Revenue growth (YoY)": "+23%",
            "Forward P/E": "28x",
            "Analyst consensus": "68% Buy — 22 analysts",
            "12M price target": "$140 avg → +24% upside",
            "EPS growth": "First profitable year",
            "ASEAN market": "700M population, 5%+ GDP growth",
            "Free cash flow": "$1.2B (first time positive)",
        },
        "thesis": "Sea (Shopee + SeaMoney + Garena) just turned profitable for the first time. SE Asia's 700M people entering peak digital commerce years. ASEAN economies growing 5%+ annually. Deeply undervalued vs comparable US digital platforms.",
        "risks": "Garena gaming declining. Indonesia regulatory risk.",
        "horizon": "3–7 years",
    },
    {
        "ticker": "CELH", "name": "Celsius Holdings", "region": "🇺🇸 US", "sector": "Consumer Health",
        "price": 31.20, "chg": +1.8, "signal": "Watch / Accumulate", "score": 74,
        "fundamentals": {
            "Revenue growth (YoY)": "+18% (recovering from -30% dip)",
            "Forward P/E": "45x",
            "Analyst consensus": "72% Buy — 18 analysts",
            "12M price target": "$42 avg → +35% upside",
            "EPS growth": "Turning profitable",
            "Short interest": "12% — elevated (squeeze potential)",
            "Insider activity": "Buying",
        },
        "thesis": "Went through painful inventory correction at Pepsi partner but fundamentals recovering. International expansion just starting. Health energy drink category +15% annually. High short interest creates squeeze potential. Best entry point in 3 years.",
        "risks": "High short interest, distribution concentration.",
        "horizon": "2–3 years",
    },
]

# ── Stock Sell / Avoid ────────────────────────────────────────────────────────
STOCK_SELLS = [
    {
        "ticker": "INTC", "name": "Intel", "region": "🇺🇸 US", "sector": "Semiconductors",
        "price": 21.30, "chg": -0.8, "signal": "Avoid", "score": 18,
        "fundamentals": {
            "Revenue growth (YoY)": "-8%",
            "Forward P/E": "N/M (unprofitable)",
            "Analyst consensus": "62% Hold/Sell",
            "12M price target": "$24 avg → minimal upside",
            "EPS growth": "Negative — losing money",
            "Free cash flow": "-$15B (burning cash)",
            "Insider activity": "Selling",
        },
        "thesis": "Burning $15B+ cash annually rebuilding fabs. Lost AI chip war to NVDA/AMD. Foundry losing to TSMC. No clear profitability path before 2027. Revenue declining YoY. Avoid.",
        "horizon": "Avoid 12–18 months minimum",
    },
    {
        "ticker": "BABA", "name": "Alibaba", "region": "🇨🇳 China", "sector": "E-commerce",
        "price": 87.10, "chg": -2.1, "signal": "Avoid", "score": 22,
        "fundamentals": {
            "Revenue growth (YoY)": "+7%",
            "Forward P/E": "9x (value trap)",
            "Analyst consensus": "Mixed — regulatory risk",
            "12M price target": "$120 — wide range, low conviction",
            "EPS growth": "+12%",
            "Free cash flow": "$22B trailing",
            "Key risk": "CCP delisting / regulatory",
        },
        "thesis": "Looks cheap at 9x P/E but is a value trap. CCP regulatory risk is unquantifiable and permanent. US-China tensions risk forced delisting. Use VWO/EEM for EM exposure instead — same geography, lower existential risk.",
        "horizon": "Avoid — better EM options exist",
    },
    {
        "ticker": "PFE", "name": "Pfizer", "region": "🇺🇸 US", "sector": "Pharma",
        "price": 27.30, "chg": -0.6, "signal": "Reduce", "score": 29,
        "fundamentals": {
            "Revenue growth (YoY)": "-41% (COVID cliff)",
            "Forward P/E": "8x",
            "Analyst consensus": "55% Hold/Sell",
            "12M price target": "$29 — minimal upside",
            "EPS growth": "-72% YoY",
            "Free cash flow": "Sharply declining",
            "Insider activity": "Selling",
        },
        "thesis": "COVID windfall is over. Revenue -41% YoY. $43B Seagen acquisition not yet translating to growth. Pipeline weak vs LLY, MRK, ABBV. Dividend at risk if FCF keeps declining. Rotate to LLY or ABBV.",
        "horizon": "Reduce — rotate to better pharma",
    },
    {
        "ticker": "NIO", "name": "NIO", "region": "🇨🇳 China", "sector": "EV",
        "price": 3.50, "chg": -2.4, "signal": "Avoid", "score": 12,
        "fundamentals": {
            "Revenue growth (YoY)": "+18% but losses widening",
            "Forward P/E": "N/M (deeply unprofitable)",
            "Analyst consensus": "40% Buy — low conviction",
            "12M price target": "$5 (from very low base)",
            "EPS growth": "-$2.80/share loss",
            "Free cash flow": "-$3.8B (burning cash)",
            "Short interest": "8.2%",
        },
        "thesis": "Burning $3.8B cash/year competing against BYD and dozens of state-backed rivals. No profitability path before 2027. US-China tensions add geopolitical risk on top of business risk. Two reasons to avoid.",
        "horizon": "Avoid entirely",
    },
    {
        "ticker": "DIS", "name": "Disney", "region": "🇺🇸 US", "sector": "Media",
        "price": 101.30, "chg": -0.5, "signal": "Hold only", "score": 35,
        "fundamentals": {
            "Revenue growth (YoY)": "+3%",
            "Forward P/E": "18x",
            "Analyst consensus": "58% Hold",
            "12M price target": "$112 → +11% upside (weak)",
            "EPS growth": "Recovering slowly",
            "Free cash flow": "$6B trailing",
            "Linear TV (ESPN)": "Structural decline",
        },
        "thesis": "Streaming finally profitable but growth slowing. Parks near peak with no major catalyst. ESPN in structural decline. Fairly valued at best. Hold if owned — don't add. Better media exposure via content creators (NFLX).",
        "horizon": "Hold if owned, don't add",
    },
]

# ── Sector sentiment with ETF + stock picks ───────────────────────────────────
SECTOR_SENTIMENT = [
    {
        "sector": "Technology", "score": 82, "direction": "Bullish", "color": "#1D9E75",
        "etf": "QQQ / SOXX", "stock_pick": "NVDA, MSFT, APP",
        "etf_reason": "AI capex boom driving mega-cap tech earnings. Semiconductor revenue +35% YoY average.",
    },
    {
        "sector": "Defense & Aerospace", "score": 78, "direction": "Bullish", "color": "#1D9E75",
        "etf": "ITA / XAR", "stock_pick": "LMT, RTX",
        "etf_reason": "NATO at record spending. Middle East conflict sustaining demand for 5+ years.",
    },
    {
        "sector": "Healthcare", "score": 68, "direction": "Bullish", "color": "#1D9E75",
        "etf": "XLV / IBB", "stock_pick": "LLY, ABBV",
        "etf_reason": "GLP-1 drug cycle driving sector outperformance. Biotech M&A picking up.",
    },
    {
        "sector": "EM & Asia", "score": 62, "direction": "Improving", "color": "#BA7517",
        "etf": "VWO / EWJ", "stock_pick": "MELI, SE",
        "etf_reason": "Fed cuts will boost EM. Japan reforms + India growth are structural tailwinds.",
    },
    {
        "sector": "Energy", "score": 52, "direction": "Neutral", "color": "#BA7517",
        "etf": "XLE — hold only", "stock_pick": "XOM (trim on spikes)",
        "etf_reason": "Oil above $100 unsustainable. Ceasefire risk could trigger sharp correction.",
    },
    {
        "sector": "Financials", "score": 54, "direction": "Neutral", "color": "#BA7517",
        "etf": "XLF — selective", "stock_pick": "JPM only",
        "etf_reason": "Strong economy helps banks but delayed rate cuts limit upside.",
    },
    {
        "sector": "Consumer", "score": 38, "direction": "Bearish", "color": "#D85A30",
        "etf": "XLY — avoid", "stock_pick": "Avoid retail exposure",
        "etf_reason": "Oil shock eating into spending. Retail traffic slowing QoQ.",
    },
    {
        "sector": "Real Estate", "score": 30, "direction": "Bearish", "color": "#D85A30",
        "etf": "VNQ — avoid", "stock_pick": "Avoid sector",
        "etf_reason": "Commercial real estate under pressure. Rates too high for profitable refinancing.",
    },
]

# ── AI Advisor picks ──────────────────────────────────────────────────────────
ADVISOR_PICKS = [
    {
        "ticker": "VOO + QQQM", "name": "Core ETF Foundation",
        "action": "Strong Buy", "accent": "#1D9E75",
        "thesis": "60–70% of your portfolio in VOO and QQQM gives automatic exposure to the AI boom, US economic strength, and long-term compounding — without individual stock risk. These two ETFs cover 200+ companies across every major sector.",
        "horizon": "DCA monthly — 5–20 years", "allocation": "60–70% of total",
    },
    {
        "ticker": "SOXX + ITA", "name": "Thematic Growth Layer",
        "action": "Buy", "accent": "#378ADD",
        "thesis": "SOXX gives semiconductor value chain exposure (AI chips). ITA captures the defense spending wave. Both are driven by structural multi-year trends — not quarterly sentiment. Revenue for holdings growing 30-35% on average.",
        "horizon": "3–7 years", "allocation": "10–15% of total",
    },
    {
        "ticker": "VGK + EWJ", "name": "International Diversification",
        "action": "Accumulate", "accent": "#BA7517",
        "thesis": "VGK: Europe at historic valuation discount, ECB cutting rates, PMI turning. EWJ: Japan corporate reforms unlocking value — even Buffett is buying. Both add non-USD diversification and reduce US-only concentration risk.",
        "horizon": "3–5 years", "allocation": "10–15% of total",
    },
    {
        "ticker": "ASML + SAP", "name": "International Quality Stocks",
        "action": "Buy", "accent": "#7F77DD",
        "thesis": "ASML monopoly on EUV chip machines — no AI chip exists without them, €36B backlog locked. SAP runs financial systems of 80% of Fortune 500, cloud revenue growing 30% YoY. Both European — adds diversification with stronger moats than most US tech.",
        "horizon": "5–10 years", "allocation": "5–10% of total",
    },
]
