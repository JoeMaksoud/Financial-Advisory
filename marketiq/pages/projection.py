import streamlit as st
import plotly.graph_objects as go
from data.live_prices import get_prices, price_display

ALL_STOCKS = {
    "VOO":("Vanguard S&P 500 ETF",0.107,"low"),"VTI":("Vanguard Total Market",0.105,"low"),
    "QQQM":("Invesco Nasdaq-100 Mini",0.158,"mid"),"QQQ":("Invesco Nasdaq-100",0.158,"mid"),
    "SPY":("SPDR S&P 500",0.107,"low"),"SOXX":("iShares Semiconductor",0.185,"mid"),
    "ITA":("Aerospace & Defense ETF",0.112,"low"),"SCHD":("Schwab Dividend ETF",0.092,"low"),
    "VGK":("Vanguard European ETF",0.082,"mid"),"EWJ":("iShares Japan ETF",0.088,"mid"),
    "VWO":("Vanguard Emerging Markets",0.095,"high"),"VNQ":("Vanguard Real Estate",0.075,"high"),
    "GLD":("SPDR Gold ETF",0.075,"low"),"TLT":("iShares 20Y Treasury",0.045,"mid"),
    "XLE":("SPDR Energy ETF",0.095,"mid"),"ARKK":("ARK Innovation ETF",0.05,"high"),
    "MSFT":("Microsoft",0.175,"low"),"NVDA":("Nvidia",0.280,"high"),
    "GOOGL":("Alphabet / Google",0.152,"mid"),"AMZN":("Amazon",0.165,"mid"),
    "META":("Meta Platforms",0.210,"high"),"AAPL":("Apple",0.145,"low"),
    "AVGO":("Broadcom",0.220,"high"),"TSLA":("Tesla",0.120,"high"),
    "BRK.B":("Berkshire Hathaway B",0.105,"low"),"JPM":("JPMorgan Chase",0.132,"mid"),
    "ASML":("ASML Holding",0.168,"mid"),"SAP":("SAP SE",0.138,"mid"),
    "APP":("AppLovin",0.220,"high"),"MELI":("MercadoLibre",0.178,"high"),
    "SE":("Sea Limited",0.112,"high"),"CELH":("Celsius Holdings",0.142,"high"),
    "LLY":("Eli Lilly",0.185,"high"),"ABBV":("AbbVie",0.128,"mid"),
    "XOM":("ExxonMobil",0.095,"mid"),"LMT":("Lockheed Martin",0.112,"mid"),
    "NEE":("NextEra Energy",0.118,"low"),"O":("Realty Income",0.092,"low"),
    "EQIX":("Equinix",0.135,"mid"),"NFLX":("Netflix",0.175,"high"),
    "AMD":("Advanced Micro Devices",0.210,"high"),"INTC":("Intel",0.032,"high"),
    "AMAT":("Applied Materials",0.195,"high"),"TSM":("Taiwan Semiconductor",0.155,"mid"),
    "PFE":("Pfizer",0.045,"mid"),"NIO":("NIO",0.038,"high"),"BABA":("Alibaba",0.048,"high"),
    "COST":("Costco",0.138,"low"),"V":("Visa",0.148,"low"),"MA":("Mastercard",0.155,"low"),
    "UNH":("UnitedHealth",0.168,"mid"),"HD":("Home Depot",0.128,"mid"),
}

def search_stocks(q):
    qu=q.strip().upper(); ql=q.strip().lower()
    if not qu: return []
    t_hits,n_hits=[],[]
    for ticker,(name,rate,risk) in ALL_STOCKS.items():
        if ticker.startswith(qu): t_hits.append((ticker,name,rate,risk))
        elif name.lower().startswith(ql) or ql in name.lower(): n_hits.append((ticker,name,rate,risk))
    seen,out=set(),[]
    for item in t_hits+n_hits:
        if item[0] not in seen: seen.add(item[0]); out.append(item)
    return out[:8]

def _risk_style(r):
    return {"low":"background:rgba(29,158,117,0.15);color:#1D9E75;border:0.5px solid rgba(29,158,117,0.3)",
            "mid":"background:rgba(186,117,23,0.15);color:#BA7517;border:0.5px solid rgba(186,117,23,0.3)",
            "high":"background:rgba(216,90,48,0.15);color:#D85A30;border:0.5px solid rgba(216,90,48,0.3)"}.get(r,"")

def project(amount,freq,rate,years):
    months=max(1,round(years*12)); rm=(1+rate)**(1/12)-1
    value=invested=0.0; tl=[]
    for m in range(months+1):
        if freq=="One-time":
            if m==0: value=amount; invested=amount
            else: value*=(1+rm)
        elif freq=="Monthly":
            if m>0: value=(value+amount)*(1+rm); invested+=amount
        else:
            if m>0 and m%12==0: value+=amount; invested+=amount
            if m>0: value*=(1+rm)
        tl.append({"invested":round(invested),"value":round(value)})
    return {"invested":round(invested),"final":round(value),"tl":tl}

def calc_scenario(entries,mult):
    ti=tf=0.0
    for e in entries:
        info=ALL_STOCKS.get(e["ticker"],("",0.10,"mid"))
        res=project(e["amount"],e["freq"],max(0.001,info[1]*mult),e["years"])
        ti+=res["invested"]; tf+=res["final"]
    return round(ti),round(tf)

def _empty(rid):
    return {"id":rid,"search_text":"","confirmed_ticker":"","amount":1000.0,"freq":"Monthly","pval":2,"punit":"Years"}

def show():
    st.markdown('<h2 style="font-size:1.5rem;font-weight:600;letter-spacing:-0.3px;margin-bottom:4px">Projection Calculator</h2>',unsafe_allow_html=True)
    st.caption("Search any stock or ETF, set amount, frequency and period — see projected returns with fundamentals-based rates.")
    st.markdown("---")

    if "proj_rows" not in st.session_state: st.session_state["proj_rows"]=[_empty(0)]
    if "next_rid" not in st.session_state: st.session_state["next_rid"]=1
    rows=st.session_state["proj_rows"]; to_remove=None

    h1,h2,h3,h4,h5,h6,h7=st.columns([2.2,1.2,1.3,1.3,0.7,1.0,0.4])
    for col,lbl in zip([h1,h2,h3,h4,h5,h6],["Stock","Current price","Amount ($)","Frequency","Period","Unit"]):
        col.markdown(f'<span style="font-size:0.75rem;opacity:0.45;text-transform:uppercase;letter-spacing:0.06em;font-weight:600">{lbl}</span>',unsafe_allow_html=True)

    for idx,row in enumerate(rows):
        rid=row["id"]
        c1,c2,c3,c4,c5,c6,c7=st.columns([2.2,1.2,1.3,1.3,0.7,1.0,0.4])
        with c1:
            query=st.text_input(f"Stock {idx+1}",value=row.get("search_text",""),placeholder="Ticker or name…",key=f"s_{rid}",label_visibility="collapsed")
            rows[idx]["search_text"]=query; confirmed=row.get("confirmed_ticker","")
            if query and (not confirmed or query.upper()!=confirmed):
                hits=search_stocks(query)
                if hits:
                    st.markdown('<div style="background:rgba(128,128,128,0.07);border:0.5px solid rgba(128,128,128,0.18);border-radius:10px;overflow:hidden;margin-top:2px">',unsafe_allow_html=True)
                    for ticker,name,rate,risk in hits:
                        if st.button(f"{ticker}  —  {name}  ({risk} risk, avg {round(rate*100)}%/yr)",key=f"ac_{rid}_{ticker}",use_container_width=True):
                            rows[idx]["confirmed_ticker"]=ticker; rows[idx]["search_text"]=f"{ticker} — {name}"; st.rerun()
                    st.markdown("</div>",unsafe_allow_html=True)
                else: st.caption("No matches")
            elif confirmed and confirmed in ALL_STOCKS:
                info=ALL_STOCKS[confirmed]
                st.markdown(f'<div style="{_risk_style(info[2])};display:inline-block;padding:1px 9px;border-radius:20px;font-size:0.7rem;font-weight:600;margin-top:3px">{"Low" if info[2]=="low" else "Mid" if info[2]=="mid" else "High"} risk · avg {round(info[1]*100)}%/yr</div>',unsafe_allow_html=True)
        with c2:
            confirmed=rows[idx].get("confirmed_ticker","")
            if confirmed and confirmed in ALL_STOCKS:
                pdata=get_prices([confirmed]); p_str,chg_str,chg_col,lbl,icon=price_display(confirmed,pdata)
                st.markdown(f'<div style="background:rgba(128,128,128,0.07);border:0.5px solid rgba(128,128,128,0.15);border-radius:10px;padding:7px 12px;margin-top:1px"><div style="font-weight:700;font-size:0.95rem">{p_str}</div><div style="font-size:0.72rem;color:{chg_col}">{chg_str} <span style="opacity:0.4">{icon} {lbl}</span></div></div>',unsafe_allow_html=True)
            else:
                st.markdown('<div style="background:rgba(128,128,128,0.04);border:0.5px solid rgba(128,128,128,0.1);border-radius:10px;padding:7px 12px;opacity:0.35;font-size:0.8rem">—</div>',unsafe_allow_html=True)
        with c3: rows[idx]["amount"]=st.number_input(f"A{idx}",min_value=1.0,value=float(row.get("amount",1000)),step=50.0,key=f"a_{rid}",label_visibility="collapsed",format="%.0f")
        with c4: rows[idx]["freq"]=st.selectbox(f"F{idx}",["Monthly","Yearly","One-time"],index=["Monthly","Yearly","One-time"].index(row.get("freq","Monthly")),key=f"f_{rid}",label_visibility="collapsed")
        with c5: rows[idx]["pval"]=st.number_input(f"P{idx}",min_value=1,max_value=50,value=int(row.get("pval",2)),step=1,key=f"pv_{rid}",label_visibility="collapsed")
        with c6: rows[idx]["punit"]=st.selectbox(f"U{idx}",["Years","Months"],index=["Years","Months"].index(row.get("punit","Years")),key=f"pu_{rid}",label_visibility="collapsed")
        with c7:
            st.markdown("<div style='height:6px'></div>",unsafe_allow_html=True)
            if len(rows)>1 and st.button("✕",key=f"rm_{rid}"): to_remove=idx

    if to_remove is not None: rows.pop(to_remove); st.rerun()
    ca,cb=st.columns([1,3])
    with ca:
        if st.button("+ Add stock"):
            nid=st.session_state["next_rid"]; st.session_state["next_rid"]+=1; rows.append(_empty(nid)); st.rerun()
    with cb: calculate=st.button("📊 Calculate projections",type="primary",use_container_width=True)
    if not calculate: return

    resolved,errors=[],[]
    for i,row in enumerate(rows):
        ticker=row.get("confirmed_ticker","")
        if not ticker: errors.append(f"Row {i+1}: select a stock first."); continue
        py=row["pval"]/12 if row["punit"]=="Months" else row["pval"]
        resolved.append({**row,"ticker":ticker,"years":py})
    if errors:
        for e in errors: st.error(e)
        st.stop()

    ti=tf=0; results=[]
    for e in resolved:
        info=ALL_STOCKS.get(e["ticker"],("Unknown",0.10,"mid")); res=project(e["amount"],e["freq"],info[1],e["years"])
        ti+=res["invested"]; tf+=res["final"]; results.append({"e":e,"res":res,"info":info})

    tg=tf-ti; tp=(tg/ti*100) if ti else 0
    st.markdown("---"); st.subheader("Your projection summary")
    for r in results:
        e=r["e"]; res=r["res"]; gain=res["final"]-res["invested"]
        pl=f"{e['pval']} {e['punit'].lower()}"
        invest_str=f"**${e['amount']:,.0f}** once" if e["freq"]=="One-time" else f"**${e['amount']:,.0f}** {e['freq'].lower()}"
        st.success(f"If you invest {invest_str} in **{e['ticker']}** ({r['info'][0]}) for **{pl}**, projected gain: **+${gain:,.0f}** on top of **${res['invested']:,.0f}** invested → total **${res['final']:,.0f}**.")
    if len(results)>1:
        st.info(f"**Combined:** invest **${ti:,.0f}** → end with **${tf:,.0f}** → gain **+${tg:,.0f}** ({tp:.1f}%)")

    st.markdown("&nbsp;"); m1,m2,m3,m4=st.columns(4)
    m1.metric("Total invested",f"${ti:,.0f}"); m2.metric("Projected gain",f"+${tg:,.0f}"); m3.metric("Final portfolio",f"${tf:,.0f}"); m4.metric("Total return",f"+{tp:.1f}%")

    max_months=max(round(r["e"]["years"]*12) for r in results); cv=[];ci=[]
    for m in range(max_months+1):
        v=inv=0
        for r in results:
            tl=r["res"]["tl"]; idx2=min(m,len(tl)-1); v+=tl[idx2]["value"]; inv+=tl[idx2]["invested"]
        cv.append(v); ci.append(inv)
    xl=[f"M{m}" if max_months<=24 and m>0 else ("Now" if m==0 and max_months<=24 else (f"Yr {m//12}" if m%12==0 else "")) for m in range(max_months+1)]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=xl,y=cv,name="Portfolio value",fill="tozeroy",line=dict(color="#1D9E75",width=2.5),fillcolor="rgba(29,158,117,0.08)"))
    fig.add_trace(go.Scatter(x=xl,y=ci,name="Amount invested",fill="tozeroy",line=dict(color="#378ADD",width=1.5,dash="dash"),fillcolor="rgba(55,138,221,0.06)"))
    fig.update_layout(height=260,margin=dict(l=0,r=0,t=8,b=0),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis=dict(gridcolor="rgba(128,128,128,0.12)",tickprefix="$",tickformat=",",color="rgba(128,128,128,0.7)"),xaxis=dict(gridcolor="rgba(128,128,128,0.12)",color="rgba(128,128,128,0.7)"),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0))
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("---"); st.subheader("Per-stock breakdown")
    for r in results:
        e=r["e"]; res=r["res"]; gain=res["final"]-res["invested"]; gp=(gain/res["invested"]*100) if res["invested"] else 0
        pl=f"{e['pval']} {e['punit'].lower()}"; ca,cb,cc,cd=st.columns([2,1,1,1])
        ca.markdown(f"**{e['ticker']}** — {r['info'][0]}  \n<span style='font-size:0.78rem;opacity:0.5'>{e['freq']} · {pl} · {round(r['info'][1]*100)}% avg/yr</span>",unsafe_allow_html=True)
        cb.metric("Invested",f"${res['invested']:,.0f}"); cc.metric("Gain",f"+${gain:,.0f}",f"+{gp:.1f}%"); cd.metric("Total",f"${res['final']:,.0f}")
    st.markdown("---"); st.subheader("Bear / base / bull scenarios")
    b_inv,b_fin=calc_scenario(resolved,0.5); ba_inv,ba_fin=calc_scenario(resolved,1.0); bu_inv,bu_fin=calc_scenario(resolved,1.5)
    sc1,sc2,sc3=st.columns(3)
    with sc1: st.markdown("#### 🐻 Bear"); st.markdown("Half expected returns."); st.metric("Final",f"${b_fin:,.0f}",f"+${b_fin-b_inv:,.0f}")
    with sc2: st.markdown("#### 📊 Base"); st.markdown("Historical average returns."); st.metric("Final",f"${ba_fin:,.0f}",f"+${ba_fin-ba_inv:,.0f}")
    with sc3: st.markdown("#### 🐂 Bull"); st.markdown("Strong AI cycle, rate cuts."); st.metric("Final",f"${bu_fin:,.0f}",f"+${bu_fin-bu_inv:,.0f}")
    st.caption("⚠️ Bear/base/bull = 0.5×/1×/1.5× variance on historical rates. Not financial advice.")
