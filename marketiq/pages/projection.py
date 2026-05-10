import streamlit as st
import plotly.graph_objects as go
from data.live_prices import get_prices, price_display

# ── Full stock universe ───────────────────────────────────────────────────────
ALL_STOCKS = {
    "VOO":   ("Vanguard S&P 500 ETF",        0.107, "low"),
    "VTI":   ("Vanguard Total Stock Market",  0.105, "low"),
    "QQQ":   ("Invesco Nasdaq-100 ETF",       0.158, "mid"),
    "SPY":   ("SPDR S&P 500 ETF",            0.107, "low"),
    "MSFT":  ("Microsoft",                    0.175, "low"),
    "NVDA":  ("Nvidia",                       0.280, "high"),
    "GOOGL": ("Alphabet / Google",            0.152, "mid"),
    "GOOG":  ("Alphabet / Google (C)",        0.152, "mid"),
    "AMZN":  ("Amazon",                       0.165, "mid"),
    "META":  ("Meta Platforms",               0.210, "high"),
    "AAPL":  ("Apple",                        0.145, "low"),
    "AVGO":  ("Broadcom",                     0.220, "high"),
    "TSLA":  ("Tesla",                        0.120, "high"),
    "BRK.B": ("Berkshire Hathaway B",         0.105, "low"),
    "BRK.A": ("Berkshire Hathaway A",         0.105, "low"),
    "JPM":   ("JPMorgan Chase",               0.132, "mid"),
    "V":     ("Visa",                         0.148, "low"),
    "MA":    ("Mastercard",                   0.155, "low"),
    "UNH":   ("UnitedHealth Group",           0.168, "mid"),
    "LLY":   ("Eli Lilly",                    0.185, "high"),
    "JNJ":   ("Johnson & Johnson",            0.088, "low"),
    "XOM":   ("ExxonMobil",                   0.095, "mid"),
    "NEE":   ("NextEra Energy",               0.118, "low"),
    "PG":    ("Procter & Gamble",             0.092, "low"),
    "KO":    ("Coca-Cola",                    0.082, "low"),
    "HD":    ("Home Depot",                   0.128, "mid"),
    "WMT":   ("Walmart",                      0.110, "low"),
    "COST":  ("Costco",                       0.138, "low"),
    "MCD":   ("McDonald's",                   0.105, "low"),
    "NKE":   ("Nike",                         0.098, "mid"),
    "NFLX":  ("Netflix",                      0.175, "high"),
    "DIS":   ("Disney",                       0.062, "mid"),
    "PYPL":  ("PayPal",                       0.075, "high"),
    "CRM":   ("Salesforce",                   0.145, "mid"),
    "ADBE":  ("Adobe",                        0.158, "mid"),
    "AMD":   ("Advanced Micro Devices",       0.210, "high"),
    "INTC":  ("Intel",                        0.032, "high"),
    "QCOM":  ("Qualcomm",                     0.118, "mid"),
    "AMAT":  ("Applied Materials",            0.195, "high"),
    "LRCX":  ("Lam Research",                 0.188, "high"),
    "MU":    ("Micron Technology",            0.165, "high"),
    "TSM":   ("Taiwan Semiconductor",         0.155, "mid"),
    "ASML":  ("ASML Holding",                 0.168, "mid"),
    "LMT":   ("Lockheed Martin",              0.112, "mid"),
    "RTX":   ("Raytheon Technologies",        0.108, "mid"),
    "NOC":   ("Northrop Grumman",             0.115, "mid"),
    "GLD":   ("SPDR Gold ETF",                0.075, "low"),
    "SLV":   ("iShares Silver ETF",           0.055, "mid"),
    "O":     ("Realty Income",                0.092, "low"),
    "EQIX":  ("Equinix",                      0.135, "mid"),
    "AMT":   ("American Tower",               0.118, "mid"),
    "GS":    ("Goldman Sachs",                0.138, "mid"),
    "BAC":   ("Bank of America",              0.112, "mid"),
    "WFC":   ("Wells Fargo",                  0.095, "mid"),
    "C":     ("Citigroup",                    0.088, "mid"),
    "AXP":   ("American Express",             0.142, "mid"),
    "PFE":   ("Pfizer",                       0.045, "mid"),
    "MRK":   ("Merck",                        0.105, "low"),
    "ABBV":  ("AbbVie",                       0.128, "mid"),
    "BMY":   ("Bristol-Myers Squibb",         0.078, "mid"),
    "CVX":   ("Chevron",                      0.088, "mid"),
    "COP":   ("ConocoPhillips",               0.115, "mid"),
    "SLB":   ("Schlumberger",                 0.095, "mid"),
    "UBER":  ("Uber",                         0.145, "high"),
    "ABNB":  ("Airbnb",                       0.112, "high"),
    "SHOP":  ("Shopify",                      0.168, "high"),
    "COIN":  ("Coinbase",                     0.142, "high"),
    "PLTR":  ("Palantir",                     0.188, "high"),
    "SNOW":  ("Snowflake",                    0.132, "high"),
    "DDOG":  ("Datadog",                      0.155, "high"),
    "NET":   ("Cloudflare",                   0.162, "high"),
    "ZS":    ("Zscaler",                      0.148, "high"),
    "CRWD":  ("CrowdStrike",                  0.172, "high"),
    "NOW":   ("ServiceNow",                   0.165, "mid"),
    "WDAY":  ("Workday",                      0.138, "mid"),
    "MELI":  ("MercadoLibre",                 0.178, "high"),
    "BABA":  ("Alibaba",                      0.048, "high"),
    "NIO":   ("NIO",                          0.038, "high"),
    "RIVN":  ("Rivian",                       0.052, "high"),
    "F":     ("Ford Motor",                   0.062, "mid"),
    "GM":    ("General Motors",               0.075, "mid"),
    "TM":    ("Toyota",                       0.092, "low"),
    "BA":    ("Boeing",                       0.058, "high"),
    "CAT":   ("Caterpillar",                  0.128, "mid"),
    "DE":    ("John Deere",                   0.132, "mid"),
    "HON":   ("Honeywell",                    0.108, "low"),
    "SOFI":  ("SoFi Technologies",            0.095, "high"),
    "NU":    ("Nu Holdings",                  0.125, "high"),
}


def search_stocks(query: str) -> list:
    q_up  = query.strip().upper()
    q_low = query.strip().lower()
    if not q_up:
        return []
    ticker_hits, name_hits = [], []
    for ticker, (name, rate, risk) in ALL_STOCKS.items():
        if ticker.startswith(q_up):
            ticker_hits.append((ticker, name, rate, risk))
        elif name.lower().startswith(q_low) or q_low in name.lower():
            name_hits.append((ticker, name, rate, risk))
    seen, out = set(), []
    for item in ticker_hits + name_hits:
        if item[0] not in seen:
            seen.add(item[0]); out.append(item)
    return out[:8]


def _risk_style(risk):
    return {
        "low":  "background:rgba(29,158,117,0.15);color:#1D9E75;border:1px solid rgba(29,158,117,0.3)",
        "mid":  "background:rgba(186,117,23,0.15);color:#BA7517;border:1px solid rgba(186,117,23,0.3)",
        "high": "background:rgba(216,90,48,0.15);color:#D85A30;border:1px solid rgba(216,90,48,0.3)",
    }.get(risk, "")


def _risk_label(risk):
    return {"low":"Low risk","mid":"Mid risk","high":"High risk"}.get(risk, risk)


def project_stock(amount, freq, rate_annual, period_years):
    months = max(1, round(period_years * 12))
    rm = (1 + rate_annual) ** (1/12) - 1
    value = invested = 0.0
    tl = []
    for m in range(months + 1):
        if freq == "One-time":
            if m == 0: value = amount; invested = amount
            else:      value *= (1 + rm)
        elif freq == "Monthly":
            if m > 0:  value = (value + amount) * (1 + rm); invested += amount
        else:
            if m > 0 and m % 12 == 0: value += amount; invested += amount
            if m > 0: value *= (1 + rm)
        tl.append({"invested": round(invested), "value": round(value)})
    return {"invested": round(invested), "final_value": round(value), "timeline": tl}


def calc_scenario(entries, mult):
    ti = tf = 0.0
    for e in entries:
        info = ALL_STOCKS.get(e["ticker"], ("", 0.10, "mid"))
        res  = project_stock(e["amount"], e["freq"], max(0.001, info[1]*mult), e["period_years"])
        ti  += res["invested"]; tf += res["final_value"]
    return round(ti), round(tf)


def _empty_row(rid):
    return {"id": rid, "search_text": "", "confirmed_ticker": "",
            "amount": 1000.0, "freq": "Monthly", "period_val": 2, "period_unit": "Years"}


def show():
    # ── inline autocomplete CSS ───────────────────────────────────────────────
    st.markdown("""
    <style>
    .autocomplete-wrap { position: relative; }
    .ac-dropdown {
        position: absolute; top: 100%; left: 0; right: 0; z-index: 9999;
        background: var(--background-color, #1e1e1e);
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 10px; overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        margin-top: 3px;
    }
    .ac-item {
        padding: 9px 14px; cursor: pointer; font-size: 0.85rem;
        border-bottom: 1px solid rgba(128,128,128,0.1);
        display: flex; justify-content: space-between; align-items: center;
        transition: background 0.12s;
    }
    .ac-item:last-child { border-bottom: none; }
    .ac-item:hover { background: rgba(55,138,221,0.12); }
    .ac-ticker { font-weight: 700; font-size: 0.88rem; }
    .ac-name   { opacity: 0.55; font-size: 0.78rem; margin-left: 8px; }
    .ac-rate   { opacity: 0.45; font-size: 0.72rem; }
    .price-chip {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(128,128,128,0.08);
        border: 1px solid rgba(128,128,128,0.15);
        border-radius: 10px; padding: 6px 14px;
        font-size: 0.88rem; margin-bottom: 4px;
    }
    .price-chip .pc-ticker { font-weight: 700; }
    .price-chip .pc-price  { font-weight: 600; font-size: 1rem; }
    .price-chip .pc-chg    { font-size: 0.78rem; }
    .price-chip .pc-live   { font-size: 0.68rem; opacity: 0.4; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="font-size:1.4rem;font-weight:500;margin-bottom:4px">📊 Projection Calculator</h2>', unsafe_allow_html=True)
    st.caption("Search any stock by name or ticker, set your amount, frequency, and period — then see projected returns.")
    st.markdown("---")

    if "proj_rows" not in st.session_state:
        st.session_state["proj_rows"] = [_empty_row(0)]
    if "next_row_id" not in st.session_state:
        st.session_state["next_row_id"] = 1

    rows    = st.session_state["proj_rows"]
    to_remove = None

    # ── column headers ────────────────────────────────────────────────────────
    h1,h2,h3,h4,h5,h6,h7 = st.columns([2.2, 1.2, 1.3, 1.3, 0.7, 1.0, 0.4])
    for col, lbl in zip([h1,h2,h3,h4,h5,h6],
                        ["Stock","Current price","Amount ($)","Frequency","Period","Unit"]):
        col.markdown(
            f'<span style="font-size:0.75rem;opacity:0.45;text-transform:uppercase;'
            f'letter-spacing:0.06em;font-weight:600">{lbl}</span>',
            unsafe_allow_html=True)

    # ── rows ──────────────────────────────────────────────────────────────────
    for idx, row in enumerate(rows):
        rid = row["id"]
        c1,c2,c3,c4,c5,c6,c7 = st.columns([2.2, 1.2, 1.3, 1.3, 0.7, 1.0, 0.4])

        with c1:
            query = st.text_input(
                f"Stock {idx+1}",
                value=row.get("search_text",""),
                placeholder="Type ticker or company name…",
                key=f"search_{rid}",
                label_visibility="collapsed",
            )
            rows[idx]["search_text"] = query
            confirmed = row.get("confirmed_ticker","")

            # ── autocomplete dropdown ─────────────────────────────────────────
            if query and (not confirmed or query.upper() != confirmed):
                hits = search_stocks(query)
                if hits:
                    # render clickable suggestion buttons that look like a dropdown
                    st.markdown(
                        '<div style="background:rgba(128,128,128,0.07);border:1px solid '
                        'rgba(128,128,128,0.18);border-radius:10px;overflow:hidden;margin-top:2px;">',
                        unsafe_allow_html=True)
                    for ticker, name, rate, risk in hits:
                        rs = _risk_label(risk)
                        label = f"{ticker}  —  {name}  ({rs}, avg {round(rate*100)}%/yr)"
                        if st.button(label, key=f"ac_{rid}_{ticker}",
                                     use_container_width=True):
                            rows[idx]["confirmed_ticker"] = ticker
                            rows[idx]["search_text"]      = f"{ticker} — {name}"
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.caption("No matches found")

            elif confirmed and confirmed in ALL_STOCKS:
                info = ALL_STOCKS[confirmed]
                rs   = _risk_label(info[2])
                st.markdown(
                    f'<div style="{_risk_style(info[2])};display:inline-block;padding:1px 9px;'
                    f'border-radius:20px;font-size:0.7rem;font-weight:600;margin-top:3px">'
                    f'{rs} &nbsp;·&nbsp; avg {round(info[1]*100)}%/yr</div>',
                    unsafe_allow_html=True)

        # ── live price chip ───────────────────────────────────────────────────
        with c2:
            confirmed = rows[idx].get("confirmed_ticker","")
            if confirmed and confirmed in ALL_STOCKS:
                live_data = get_prices([confirmed])
                p_str, chg_str, chg_color, is_live = price_display(confirmed, live_data)
                live_dot = "🟢" if is_live else "⚪"
                st.markdown(
                    f'<div style="background:rgba(128,128,128,0.07);border:1px solid '
                    f'rgba(128,128,128,0.15);border-radius:10px;padding:7px 12px;margin-top:1px;">'
                    f'<div style="font-weight:700;font-size:0.95rem">{p_str}</div>'
                    f'<div style="font-size:0.72rem;color:{chg_color}">'
                    f'{chg_str} &nbsp;<span style="opacity:0.4">{live_dot}</span></div>'
                    f'</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="background:rgba(128,128,128,0.04);border:1px solid '
                    'rgba(128,128,128,0.1);border-radius:10px;padding:7px 12px;'
                    'opacity:0.35;font-size:0.8rem;margin-top:1px;">—</div>',
                    unsafe_allow_html=True)

        with c3:
            rows[idx]["amount"] = st.number_input(
                f"Amt {idx+1}", min_value=1.0,
                value=float(row.get("amount",1000)),
                step=50.0, key=f"amt_{rid}",
                label_visibility="collapsed", format="%.0f")

        with c4:
            rows[idx]["freq"] = st.selectbox(
                f"Frq {idx+1}", ["Monthly","Yearly","One-time"],
                index=["Monthly","Yearly","One-time"].index(row.get("freq","Monthly")),
                key=f"frq_{rid}", label_visibility="collapsed")

        with c5:
            rows[idx]["period_val"] = st.number_input(
                f"Prd {idx+1}", min_value=1, max_value=50,
                value=int(row.get("period_val",2)),
                step=1, key=f"pv_{rid}", label_visibility="collapsed")

        with c6:
            rows[idx]["period_unit"] = st.selectbox(
                f"Unt {idx+1}", ["Years","Months"],
                index=["Years","Months"].index(row.get("period_unit","Years")),
                key=f"pu_{rid}", label_visibility="collapsed")

        with c7:
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if len(rows) > 1 and st.button("✕", key=f"rm_{rid}"):
                to_remove = idx

    if to_remove is not None:
        rows.pop(to_remove); st.rerun()

    col_add, col_calc = st.columns([1,3])
    with col_add:
        if st.button("+ Add stock"):
            nid = st.session_state["next_row_id"]
            st.session_state["next_row_id"] += 1
            rows.append(_empty_row(nid)); st.rerun()
    with col_calc:
        calculate = st.button("📊 Calculate projections", type="primary", use_container_width=True)

    if not calculate:
        return

    # ── validate ──────────────────────────────────────────────────────────────
    resolved, errors = [], []
    for i, row in enumerate(rows):
        ticker = row.get("confirmed_ticker","")
        if not ticker:
            errors.append(f"Row {i+1}: please search and select a stock first.")
            continue
        py = row["period_val"]/12 if row["period_unit"]=="Months" else row["period_val"]
        resolved.append({**row, "ticker": ticker, "period_years": py})

    if errors:
        for e in errors: st.error(e)
        st.stop()

    # ── calculate ─────────────────────────────────────────────────────────────
    total_invested = total_final = 0
    results = []
    for e in resolved:
        info = ALL_STOCKS.get(e["ticker"],("Unknown",0.10,"mid"))
        res  = project_stock(e["amount"], e["freq"], info[1], e["period_years"])
        total_invested += res["invested"]; total_final += res["final_value"]
        results.append({"entry":e,"res":res,"info":info})

    total_gain = total_final - total_invested
    total_pct  = (total_gain/total_invested*100) if total_invested else 0

    st.markdown("---")
    st.subheader("Your projection summary")
    for r in results:
        e=r["entry"]; res=r["res"]
        gain=res["final_value"]-res["invested"]
        period_label=f"{e['period_val']} {e['period_unit'].lower()}"
        invest_str=(f"**${e['amount']:,.0f}** once" if e["freq"]=="One-time"
                    else f"**${e['amount']:,.0f}** {e['freq'].lower()}")
        st.success(
            f"If you invest {invest_str} in **{e['ticker']}** ({r['info'][0]}) "
            f"for **{period_label}**, you are projected to make **+${gain:,.0f}** "
            f"in addition to the **${res['invested']:,.0f}** invested — "
            f"totalling **${res['final_value']:,.0f}**.")

    if len(results)>1:
        st.info(f"**Combined:** invest **${total_invested:,.0f}** → end with **${total_final:,.0f}** → gain **+${total_gain:,.0f}** ({total_pct:.1f}%)")

    st.markdown("&nbsp;")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total invested",  f"${total_invested:,.0f}")
    m2.metric("Projected gain",  f"+${total_gain:,.0f}")
    m3.metric("Final portfolio", f"${total_final:,.0f}")
    m4.metric("Total return",    f"+{total_pct:.1f}%")

    # chart
    max_months = max(round(r["entry"]["period_years"]*12) for r in results)
    cv=[];ci=[]
    for m in range(max_months+1):
        v=inv=0
        for r in results:
            tl=r["res"]["timeline"]; idx2=min(m,len(tl)-1)
            v+=tl[idx2]["value"]; inv+=tl[idx2]["invested"]
        cv.append(v); ci.append(inv)

    xl=[]
    for m in range(max_months+1):
        if max_months<=24: xl.append(f"M{m}" if m>0 else "Now")
        else: xl.append(f"Yr {m//12}" if m%12==0 else "")

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=xl,y=cv,name="Portfolio value",fill="tozeroy",
        line=dict(color="#1D9E75",width=2.5),fillcolor="rgba(29,158,117,0.08)"))
    fig.add_trace(go.Scatter(x=xl,y=ci,name="Amount invested",fill="tozeroy",
        line=dict(color="#378ADD",width=1.5,dash="dash"),fillcolor="rgba(55,138,221,0.06)"))
    fig.update_layout(height=260,margin=dict(l=0,r=0,t=8,b=0),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(128,128,128,0.12)",tickprefix="$",tickformat=",",
                   color="rgba(128,128,128,0.7)"),
        xaxis=dict(gridcolor="rgba(128,128,128,0.12)",color="rgba(128,128,128,0.7)"),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0))
    st.plotly_chart(fig,use_container_width=True)

    # per-stock breakdown
    st.markdown("---"); st.subheader("Per-stock breakdown")
    for r in results:
        e=r["entry"]; res=r["res"]
        gain=res["final_value"]-res["invested"]
        gp=(gain/res["invested"]*100) if res["invested"] else 0
        pl=f"{e['period_val']} {e['period_unit'].lower()}"
        ca,cb,cc,cd=st.columns([2,1,1,1])
        ca.markdown(f"**{e['ticker']}** — {r['info'][0]}  \n"
                    f"<span style='font-size:0.78rem;opacity:0.5'>{e['freq']} · {pl} · {round(r['info'][1]*100)}% avg/yr</span>",
                    unsafe_allow_html=True)
        cb.metric("Invested",f"${res['invested']:,.0f}")
        cc.metric("Gain",f"+${gain:,.0f}",f"+{gp:.1f}%")
        cd.metric("Total",f"${res['final_value']:,.0f}")

    # scenarios
    st.markdown("---"); st.subheader("Bear / base / bull scenarios")
    b_inv,b_fin=calc_scenario(resolved,0.5)
    ba_inv,ba_fin=calc_scenario(resolved,1.0)
    bu_inv,bu_fin=calc_scenario(resolved,1.5)
    sc1,sc2,sc3=st.columns(3)
    with sc1:
        st.markdown("#### 🐻 Bear case")
        st.markdown("Market underperforms. Half of expected returns.")
        st.metric("Final value",f"${b_fin:,.0f}",f"+${b_fin-b_inv:,.0f}")
    with sc2:
        st.markdown("#### 📊 Base case")
        st.markdown("Historical average returns. Most likely outcome.")
        st.metric("Final value",f"${ba_fin:,.0f}",f"+${ba_fin-ba_inv:,.0f}")
    with sc3:
        st.markdown("#### 🐂 Bull case")
        st.markdown("Strong AI cycle, rate cuts, outperformance.")
        st.metric("Final value",f"${bu_fin:,.0f}",f"+${bu_fin-bu_inv:,.0f}")
    st.caption("⚠️ Bear/base/bull = 0.5×/1×/1.5× variance on historical returns. Not financial advice.")
