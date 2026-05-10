import streamlit as st
import plotly.graph_objects as go
from data.stock_data import STOCKS
from data.live_prices import get_prices, price_display

# ── Extended stock universe for search ────────────────────────────────────────
ALL_STOCKS = {
    "VOO":   ("Vanguard S&P 500 ETF",         0.107, "low"),
    "VTI":   ("Vanguard Total Stock Market",   0.105, "low"),
    "QQQ":   ("Invesco Nasdaq-100 ETF",        0.158, "mid"),
    "SPY":   ("SPDR S&P 500 ETF",             0.107, "low"),
    "MSFT":  ("Microsoft",                     0.175, "low"),
    "NVDA":  ("Nvidia",                        0.280, "high"),
    "GOOGL": ("Alphabet / Google",             0.152, "mid"),
    "GOOG":  ("Alphabet / Google (C)",         0.152, "mid"),
    "AMZN":  ("Amazon",                        0.165, "mid"),
    "META":  ("Meta Platforms",                0.210, "high"),
    "AAPL":  ("Apple",                         0.145, "low"),
    "AVGO":  ("Broadcom",                      0.220, "high"),
    "TSLA":  ("Tesla",                         0.120, "high"),
    "BRK.B": ("Berkshire Hathaway B",          0.105, "low"),
    "BRK.A": ("Berkshire Hathaway A",          0.105, "low"),
    "JPM":   ("JPMorgan Chase",                0.132, "mid"),
    "V":     ("Visa",                          0.148, "low"),
    "MA":    ("Mastercard",                    0.155, "low"),
    "UNH":   ("UnitedHealth Group",            0.168, "mid"),
    "LLY":   ("Eli Lilly",                     0.185, "high"),
    "JNJ":   ("Johnson & Johnson",             0.088, "low"),
    "XOM":   ("ExxonMobil",                    0.095, "mid"),
    "NEE":   ("NextEra Energy",                0.118, "low"),
    "PG":    ("Procter & Gamble",              0.092, "low"),
    "KO":    ("Coca-Cola",                     0.082, "low"),
    "HD":    ("Home Depot",                    0.128, "mid"),
    "WMT":   ("Walmart",                       0.110, "low"),
    "COST":  ("Costco",                        0.138, "low"),
    "MCD":   ("McDonald's",                    0.105, "low"),
    "NKE":   ("Nike",                          0.098, "mid"),
    "NFLX":  ("Netflix",                       0.175, "high"),
    "DIS":   ("Disney",                        0.062, "mid"),
    "PYPL":  ("PayPal",                        0.075, "high"),
    "CRM":   ("Salesforce",                    0.145, "mid"),
    "ADBE":  ("Adobe",                         0.158, "mid"),
    "AMD":   ("Advanced Micro Devices",        0.210, "high"),
    "INTC":  ("Intel",                         0.032, "high"),
    "QCOM":  ("Qualcomm",                      0.118, "mid"),
    "AMAT":  ("Applied Materials",             0.195, "high"),
    "LRCX":  ("Lam Research",                  0.188, "high"),
    "MU":    ("Micron Technology",             0.165, "high"),
    "TSM":   ("Taiwan Semiconductor",          0.155, "mid"),
    "ASML":  ("ASML Holding",                  0.168, "mid"),
    "LMT":   ("Lockheed Martin",               0.112, "mid"),
    "RTX":   ("Raytheon Technologies",         0.108, "mid"),
    "NOC":   ("Northrop Grumman",              0.115, "mid"),
    "GLD":   ("SPDR Gold ETF",                 0.075, "low"),
    "SLV":   ("iShares Silver ETF",            0.055, "mid"),
    "O":     ("Realty Income",                 0.092, "low"),
    "EQIX":  ("Equinix",                       0.135, "mid"),
    "AMT":   ("American Tower",                0.118, "mid"),
    "GS":    ("Goldman Sachs",                 0.138, "mid"),
    "BAC":   ("Bank of America",               0.112, "mid"),
    "WFC":   ("Wells Fargo",                   0.095, "mid"),
    "C":     ("Citigroup",                     0.088, "mid"),
    "AXP":   ("American Express",              0.142, "mid"),
    "PFE":   ("Pfizer",                        0.045, "mid"),
    "MRK":   ("Merck",                         0.105, "low"),
    "ABBV":  ("AbbVie",                        0.128, "mid"),
    "BMY":   ("Bristol-Myers Squibb",          0.078, "mid"),
    "CVX":   ("Chevron",                       0.088, "mid"),
    "COP":   ("ConocoPhillips",                0.115, "mid"),
    "SLB":   ("Schlumberger",                  0.095, "mid"),
    "UBER":  ("Uber",                          0.145, "high"),
    "ABNB":  ("Airbnb",                        0.112, "high"),
    "SHOP":  ("Shopify",                       0.168, "high"),
    "COIN":  ("Coinbase",                      0.142, "high"),
    "PLTR":  ("Palantir",                      0.188, "high"),
    "SNOW":  ("Snowflake",                     0.132, "high"),
    "DDOG":  ("Datadog",                       0.155, "high"),
    "NET":   ("Cloudflare",                    0.162, "high"),
    "ZS":    ("Zscaler",                       0.148, "high"),
    "CRWD":  ("CrowdStrike",                   0.172, "high"),
    "NOW":   ("ServiceNow",                    0.165, "mid"),
    "WDAY":  ("Workday",                       0.138, "mid"),
    "MELI":  ("MercadoLibre",                  0.178, "high"),
    "BABA":  ("Alibaba",                       0.048, "high"),
    "NIO":   ("NIO",                           0.038, "high"),
    "RIVN":  ("Rivian",                        0.052, "high"),
    "F":     ("Ford Motor",                    0.062, "mid"),
    "GM":    ("General Motors",                0.075, "mid"),
    "TM":    ("Toyota",                        0.092, "low"),
    "BA":    ("Boeing",                        0.058, "high"),
    "CAT":   ("Caterpillar",                   0.128, "mid"),
    "DE":    ("John Deere",                    0.132, "mid"),
    "HON":   ("Honeywell",                     0.108, "low"),
    "SOFI":  ("SoFi Technologies",             0.095, "high"),
    "NU":    ("Nu Holdings",                   0.125, "high"),
}


def search_stocks(query: str) -> list:
    q_upper = query.strip().upper()
    q_lower = query.strip().lower()
    if not q_upper:
        return []
    ticker_hits, name_hits = [], []
    for ticker, (name, rate, risk) in ALL_STOCKS.items():
        label = f"{ticker} — {name}"
        if ticker.startswith(q_upper):
            ticker_hits.append((ticker, label))
        elif name.lower().startswith(q_lower) or q_lower in name.lower():
            name_hits.append((ticker, label))
    seen, results = set(), []
    for item in ticker_hits + name_hits:
        if item[0] not in seen:
            seen.add(item[0])
            results.append(item)
    return results[:8]


def project_stock(amount, freq, rate_annual, period_years):
    months = max(1, round(period_years * 12))
    rate_monthly = (1 + rate_annual) ** (1 / 12) - 1
    value, invested = 0.0, 0.0
    timeline = []
    for m in range(months + 1):
        if freq == "One-time":
            if m == 0:
                value = amount; invested = amount
            else:
                value *= (1 + rate_monthly)
        elif freq == "Monthly":
            if m > 0:
                value = (value + amount) * (1 + rate_monthly)
                invested += amount
        else:
            if m > 0 and m % 12 == 0:
                value += amount; invested += amount
            if m > 0:
                value *= (1 + rate_monthly)
        timeline.append({"invested": round(invested), "value": round(value)})
    return {"invested": round(invested), "final_value": round(value), "timeline": timeline}


def calc_scenario(entries, mult):
    ti, tf = 0.0, 0.0
    for e in entries:
        info = ALL_STOCKS.get(e["ticker"], ("", 0.10, "mid"))
        res = project_stock(e["amount"], e["freq"], max(0.001, info[1] * mult), e["period_years"])
        ti += res["invested"]; tf += res["final_value"]
    return round(ti), round(tf)


def _risk_badge(risk):
    colors = {"low": ("#d1fae5","#065f46"), "mid": ("#fef3c7","#92400e"), "high": ("#fee2e2","#991b1b")}
    bg, fg = colors.get(risk, ("#f3f4f6","#374151"))
    label = {"low":"Low risk","mid":"Mid risk","high":"High risk"}.get(risk, risk)
    return f'<span style="background:{bg};color:{fg};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:600">{label}</span>'


def _empty_row(rid):
    return {"id": rid, "search_text": "", "confirmed_ticker": "",
            "amount": 1000.0, "freq": "Monthly", "period_val": 2, "period_unit": "Years"}


def show():
    st.title("📊 Investment Projection Calculator")
    st.caption("Search any stock by name or ticker, set your amount, frequency, and period — then see projected returns.")

    st.markdown("---")

    if "proj_rows" not in st.session_state:
        st.session_state["proj_rows"] = [_empty_row(0)]
    if "next_row_id" not in st.session_state:
        st.session_state["next_row_id"] = 1

    rows = st.session_state["proj_rows"]
    to_remove = None

    # column headers
    h1, h2, h3, h4, h5, h6 = st.columns([2.5, 1.5, 1.5, 0.7, 1, 0.4])
    for col, lbl in zip([h1,h2,h3,h4,h5], ["Stock","Amount ($)","Frequency","Period","Unit"]):
        col.markdown(f"<span style='font-size:0.78rem;opacity:0.5;color:inherit;text-transform:uppercase;letter-spacing:0.05em'>{lbl}</span>", unsafe_allow_html=True)

    for idx, row in enumerate(rows):
        rid = row["id"]
        c1, c2, c3, c4, c5, c6 = st.columns([2.5, 1.5, 1.5, 0.7, 1, 0.4])

        with c1:
            query = st.text_input(
                f"Stock {idx+1}", value=row.get("search_text",""),
                placeholder="Type ticker or name…",
                key=f"search_{rid}", label_visibility="collapsed",
            )
            rows[idx]["search_text"] = query
            confirmed = row.get("confirmed_ticker", "")

            if query and (not confirmed or query.upper() != confirmed):
                hits = search_stocks(query)
                if hits:
                    options = [label for _, label in hits]
                    tickers = [t for t, _ in hits]
                    choice = st.selectbox(f"Pick {idx+1}", options=options,
                                          key=f"pick_{rid}", label_visibility="collapsed")
                    chosen = tickers[options.index(choice)]
                    rows[idx]["confirmed_ticker"] = chosen
                    info = ALL_STOCKS[chosen]
                    live_data = get_prices([chosen])
                    p_str, chg_str, chg_color, is_live = price_display(chosen, live_data)
                    live_tag = "🟢 Live" if is_live else "⚪ Ref."
                    st.markdown(
                        f'<div style="font-size:0.72rem;opacity:0.5;color:inherit;margin-top:2px">'
                        f'{_risk_badge(info[2])}&nbsp; avg {round(info[1]*100)}%/yr &nbsp;|&nbsp;'
                        f'<b style="color:#111">{p_str}</b> '
                        f'<span style="color:{chg_color}">{chg_str}</span> '
                        f'<span style="color:#aaa">{live_tag}</span></div>',
                        unsafe_allow_html=True)
                else:
                    st.caption("No matches found")
            elif confirmed and confirmed in ALL_STOCKS:
                info = ALL_STOCKS[confirmed]
                live_data = get_prices([confirmed])
                p_str, chg_str, chg_color, is_live = price_display(confirmed, live_data)
                live_tag = "🟢 Live" if is_live else "⚪ Ref."
                st.markdown(
                    f'<div style="font-size:0.72rem;opacity:0.5;color:inherit;margin-top:2px">'
                    f'{_risk_badge(info[2])}&nbsp; avg {round(info[1]*100)}%/yr &nbsp;|&nbsp;'
                    f'<b style="color:#111">{p_str}</b> '
                    f'<span style="color:{chg_color}">{chg_str}</span> '
                    f'<span style="color:#aaa">{live_tag}</span></div>',
                    unsafe_allow_html=True)

        with c2:
            rows[idx]["amount"] = st.number_input(f"Amt {idx+1}", min_value=1.0,
                value=float(row.get("amount",1000)), step=50.0,
                key=f"amt_{rid}", label_visibility="collapsed", format="%.0f")
        with c3:
            rows[idx]["freq"] = st.selectbox(f"Frq {idx+1}",
                ["Monthly","Yearly","One-time"],
                index=["Monthly","Yearly","One-time"].index(row.get("freq","Monthly")),
                key=f"frq_{rid}", label_visibility="collapsed")
        with c4:
            rows[idx]["period_val"] = st.number_input(f"Prd {idx+1}", min_value=1, max_value=50,
                value=int(row.get("period_val",2)), step=1,
                key=f"pv_{rid}", label_visibility="collapsed")
        with c5:
            rows[idx]["period_unit"] = st.selectbox(f"Unt {idx+1}", ["Years","Months"],
                index=["Years","Months"].index(row.get("period_unit","Years")),
                key=f"pu_{rid}", label_visibility="collapsed")
        with c6:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if len(rows) > 1 and st.button("✕", key=f"rm_{rid}"):
                to_remove = idx

    if to_remove is not None:
        rows.pop(to_remove)
        st.rerun()

    col_add, col_calc = st.columns([1, 3])
    with col_add:
        if st.button("+ Add stock"):
            nid = st.session_state["next_row_id"]
            st.session_state["next_row_id"] += 1
            rows.append(_empty_row(nid))
            st.rerun()
    with col_calc:
        calculate = st.button("📊 Calculate projections", type="primary", use_container_width=True)

    if not calculate:
        return

    # validate
    resolved, errors = [], []
    for i, row in enumerate(rows):
        ticker = row.get("confirmed_ticker","")
        if not ticker:
            errors.append(f"Row {i+1}: please select a stock from the search results.")
            continue
        py = row["period_val"] / 12 if row["period_unit"] == "Months" else row["period_val"]
        resolved.append({**row, "ticker": ticker, "period_years": py})
    if errors:
        for e in errors: st.error(e)
        st.stop()

    total_invested, total_final = 0, 0
    results = []
    for e in resolved:
        info = ALL_STOCKS.get(e["ticker"], ("Unknown", 0.10, "mid"))
        res = project_stock(e["amount"], e["freq"], info[1], e["period_years"])
        total_invested += res["invested"]; total_final += res["final_value"]
        results.append({"entry": e, "res": res, "info": info})

    total_gain = total_final - total_invested
    total_pct  = (total_gain / total_invested * 100) if total_invested else 0

    st.markdown("---")
    st.subheader("Your projection summary")
    for r in results:
        e = r["entry"]; res = r["res"]
        gain = res["final_value"] - res["invested"]
        period_label = f"{e['period_val']} {e['period_unit'].lower()}"
        invest_str = (f"**${e['amount']:,.0f}** once" if e["freq"]=="One-time"
                      else f"**${e['amount']:,.0f}** {e['freq'].lower()}")
        st.success(
            f"If you invest {invest_str} in **{e['ticker']}** ({r['info'][0]}) "
            f"for **{period_label}**, you are projected to make **+${gain:,.0f}** "
            f"in addition to the **${res['invested']:,.0f}** invested — totalling **${res['final_value']:,.0f}**."
        )
    if len(results) > 1:
        st.info(f"**Combined:** invest **${total_invested:,.0f}** → end with **${total_final:,.0f}** → gain **+${total_gain:,.0f}** ({total_pct:.1f}%)")

    st.markdown("&nbsp;")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total invested",  f"${total_invested:,.0f}")
    m2.metric("Projected gain",  f"+${total_gain:,.0f}")
    m3.metric("Final portfolio", f"${total_final:,.0f}")
    m4.metric("Total return",    f"+{total_pct:.1f}%")

    # chart
    max_months = max(round(r["entry"]["period_years"]*12) for r in results)
    cv, ci = [], []
    for m in range(max_months+1):
        v, inv = 0, 0
        for r in results:
            tl=r["res"]["timeline"]; idx2=min(m,len(tl)-1)
            v+=tl[idx2]["value"]; inv+=tl[idx2]["invested"]
        cv.append(v); ci.append(inv)

    xl = [f"M{m}" if max_months<=24 and m>0 else ("Now" if m==0 and max_months<=24 else (f"Yr {m//12}" if m%12==0 else "")) for m in range(max_months+1)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xl,y=cv,name="Portfolio value",fill="tozeroy",line=dict(color="#1D9E75",width=2),fillcolor="rgba(29,158,117,0.08)"))
    fig.add_trace(go.Scatter(x=xl,y=ci,name="Amount invested",fill="tozeroy",line=dict(color="#378ADD",width=1.5,dash="dash"),fillcolor="rgba(55,138,221,0.06)"))
    fig.update_layout(height=260,margin=dict(l=0,r=0,t=8,b=0),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f0f0",tickprefix="$",tickformat=","),
        xaxis=dict(gridcolor="#f0f0f0"),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0))
    st.plotly_chart(fig,use_container_width=True)

    # breakdown
    st.markdown("---")
    st.subheader("Per-stock breakdown")
    for r in results:
        e=r["entry"]; res=r["res"]
        gain=res["final_value"]-res["invested"]
        gain_pct=(gain/res["invested"]*100) if res["invested"] else 0
        period_label=f"{e['period_val']} {e['period_unit'].lower()}"
        ca,cb,cc,cd = st.columns([2,1,1,1])
        ca.markdown(f"**{e['ticker']}** — {r['info'][0]}  \n<span style='font-size:0.78rem;color:#888'>{e['freq']} · {period_label} · {round(r['info'][1]*100)}% avg/yr</span>",unsafe_allow_html=True)
        cb.metric("Invested",f"${res['invested']:,.0f}")
        cc.metric("Gain",f"+${gain:,.0f}",f"+{gain_pct:.1f}%")
        cd.metric("Total",f"${res['final_value']:,.0f}")

    # scenarios
    st.markdown("---")
    st.subheader("Bear / base / bull scenarios")
    b_inv,b_fin   = calc_scenario(resolved, 0.5)
    ba_inv,ba_fin = calc_scenario(resolved, 1.0)
    bu_inv,bu_fin = calc_scenario(resolved, 1.5)
    sc1,sc2,sc3 = st.columns(3)
    with sc1:
        st.markdown("#### 🐻 Bear case")
        st.markdown("Market underperforms. Half of expected returns.")
        st.metric("Final value",f"${b_fin:,.0f}", f"+${b_fin-b_inv:,.0f}")
    with sc2:
        st.markdown("#### 📊 Base case")
        st.markdown("Historical average returns. Most likely outcome.")
        st.metric("Final value",f"${ba_fin:,.0f}",f"+${ba_fin-ba_inv:,.0f}")
    with sc3:
        st.markdown("#### 🐂 Bull case")
        st.markdown("Strong AI cycle, rate cuts, outperformance.")
        st.metric("Final value",f"${bu_fin:,.0f}",f"+${bu_fin-bu_inv:,.0f}")
    st.caption("⚠️ Projections use historical average annual returns. Bear/base/bull = 0.5×/1×/1.5× variance. Not financial advice.")
