import streamlit as st
import plotly.graph_objects as go
import numpy as np
from data.stock_data import STOCKS


def project_stock(amount: float, freq: str, rate_annual: float, period_years: float):
    """Return monthly timeline of {invested, value} and final totals."""
    months = max(1, round(period_years * 12))
    rate_monthly = (1 + rate_annual) ** (1 / 12) - 1
    value, invested = 0.0, 0.0
    timeline = []

    for m in range(months + 1):
        if freq == "One-time":
            if m == 0:
                value = amount
                invested = amount
            else:
                value *= (1 + rate_monthly)
        elif freq == "Monthly":
            if m > 0:
                value = (value + amount) * (1 + rate_monthly)
                invested += amount
        else:  # Yearly
            if m > 0 and m % 12 == 0:
                value += amount
                invested += amount
            if m > 0:
                value *= (1 + rate_monthly)
        timeline.append({"invested": round(invested), "value": round(value)})

    return {
        "invested": round(invested),
        "final_value": round(value),
        "timeline": timeline,
    }


def calc_scenario(entries, mult: float):
    total_invested, total_final = 0.0, 0.0
    for e in entries:
        rate = max(0.001, STOCKS[e["ticker"]]["rate"] * mult)
        res = project_stock(e["amount"], e["freq"], rate, e["period_years"])
        total_invested += res["invested"]
        total_final += res["final_value"]
    return round(total_invested), round(total_final)


def show():
    st.title("📊 Investment Projection Calculator")
    st.caption(
        "Select stocks, set your amount, frequency, and period per stock — "
        "then see your projected returns with bear / base / bull scenarios."
    )

    st.markdown("---")

    # ── stock entry form ──────────────────────────────────────────────────────
    if "proj_entries" not in st.session_state:
        st.session_state["proj_entries"] = [
            {"ticker": "VOO", "amount": 1000.0, "freq": "Monthly", "period_val": 2, "period_unit": "Years"}
        ]

    entries = st.session_state["proj_entries"]

    # column headers
    h1, h2, h3, h4, h5, h6 = st.columns([2, 1.5, 1.5, 0.8, 1, 0.5])
    h1.markdown("**Stock**")
    h2.markdown("**Amount**")
    h3.markdown("**Frequency**")
    h4.markdown("**Period**")
    h5.markdown("**Unit**")
    h6.markdown("")

    to_remove = None
    for i, entry in enumerate(entries):
        c1, c2, c3, c4, c5, c6 = st.columns([2, 1.5, 1.5, 0.8, 1, 0.5])
        with c1:
            ticker = st.selectbox(
                f"Stock {i+1}", options=list(STOCKS.keys()),
                index=list(STOCKS.keys()).index(entry["ticker"]),
                key=f"ticker_{i}", label_visibility="collapsed",
                format_func=lambda k: f"{k} — {STOCKS[k]['name']}",
            )
            entries[i]["ticker"] = ticker
        with c2:
            amt = st.number_input(
                "Amount", min_value=1.0, value=float(entry["amount"]),
                step=50.0, key=f"amt_{i}", label_visibility="collapsed",
                format="%.0f",
            )
            entries[i]["amount"] = amt
        with c3:
            freq = st.selectbox(
                "Freq", ["Monthly", "Yearly", "One-time"],
                index=["Monthly", "Yearly", "One-time"].index(entry["freq"]),
                key=f"freq_{i}", label_visibility="collapsed",
            )
            entries[i]["freq"] = freq
        with c4:
            pval = st.number_input(
                "Period", min_value=1, max_value=50, value=entry["period_val"],
                step=1, key=f"pval_{i}", label_visibility="collapsed",
            )
            entries[i]["period_val"] = pval
        with c5:
            punit = st.selectbox(
                "Unit", ["Years", "Months"],
                index=["Years", "Months"].index(entry["period_unit"]),
                key=f"punit_{i}", label_visibility="collapsed",
            )
            entries[i]["period_unit"] = punit
        with c6:
            if len(entries) > 1:
                if st.button("✕", key=f"rm_{i}", help="Remove"):
                    to_remove = i

    if to_remove is not None:
        entries.pop(to_remove)
        st.rerun()

    col_add, col_calc = st.columns([1, 3])
    with col_add:
        if st.button("+ Add stock"):
            entries.append({"ticker": "MSFT", "amount": 500.0, "freq": "Monthly", "period_val": 2, "period_unit": "Years"})
            st.rerun()
    with col_calc:
        calculate = st.button("📊 Calculate projections", type="primary", use_container_width=True)

    # ── results ───────────────────────────────────────────────────────────────
    if calculate:
        # resolve period to years
        resolved = []
        for e in entries:
            py = e["period_val"] / 12 if e["period_unit"] == "Months" else e["period_val"]
            resolved.append({**e, "period_years": py})

        total_invested, total_final = 0, 0
        results = []
        for e in resolved:
            info = STOCKS[e["ticker"]]
            res = project_stock(e["amount"], e["freq"], info["rate"], e["period_years"])
            total_invested += res["invested"]
            total_final += res["final_value"]
            results.append({"entry": e, "res": res, "info": info})

        total_gain = total_final - total_invested
        total_pct  = (total_gain / total_invested * 100) if total_invested else 0

        st.markdown("---")

        # ── plain-English summary ────────────────────────────────────────────
        st.subheader("Your projection summary")
        for r in results:
            e    = r["entry"]
            res  = r["res"]
            gain = res["final_value"] - res["invested"]
            freq_str = e["freq"].lower()
            period_label = f"{e['period_val']} {e['period_unit'].lower()}"
            if e["freq"] == "One-time":
                invest_str = f"**${e['amount']:,.0f}** once"
            else:
                invest_str = f"**${e['amount']:,.0f}** {freq_str}"
            st.success(
                f"If you invest {invest_str} in **{e['ticker']}** for **{period_label}**, "
                f"you are projected to make **+${gain:,.0f}** in addition to the "
                f"**${res['invested']:,.0f}** invested — totalling **${res['final_value']:,.0f}**."
            )

        if len(results) > 1:
            st.info(
                f"**Combined across all stocks:** you invest **${total_invested:,.0f}** total "
                f"and are projected to end with **${total_final:,.0f}** — "
                f"a gain of **+${total_gain:,.0f}** ({total_pct:.1f}% return)."
            )

        # ── summary metrics ──────────────────────────────────────────────────
        st.markdown("&nbsp;")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total invested",  f"${total_invested:,.0f}")
        m2.metric("Projected gain",  f"+${total_gain:,.0f}")
        m3.metric("Final portfolio", f"${total_final:,.0f}")
        m4.metric("Total return",    f"+{total_pct:.1f}%")

        # ── growth chart ─────────────────────────────────────────────────────
        st.markdown("&nbsp;")
        max_months = max(round(r["entry"]["period_years"] * 12) for r in results)
        combined_v, combined_i = [], []
        for m in range(max_months + 1):
            v, inv = 0, 0
            for r in results:
                tl  = r["res"]["timeline"]
                idx = min(m, len(tl) - 1)
                v   += tl[idx]["value"]
                inv += tl[idx]["invested"]
            combined_v.append(v)
            combined_i.append(inv)

        x_labels = []
        for m in range(max_months + 1):
            if max_months <= 24:
                x_labels.append(f"M{m}" if m > 0 else "Now")
            else:
                x_labels.append(f"Yr {m//12}" if m % 12 == 0 else "")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_labels, y=combined_v, name="Portfolio value",
            fill="tozeroy", line=dict(color="#1D9E75", width=2),
            fillcolor="rgba(29,158,117,0.08)",
        ))
        fig.add_trace(go.Scatter(
            x=x_labels, y=combined_i, name="Amount invested",
            fill="tozeroy", line=dict(color="#378ADD", width=1.5, dash="dash"),
            fillcolor="rgba(55,138,221,0.06)",
        ))
        fig.update_layout(
            height=260, margin=dict(l=0, r=0, t=8, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#f0f0f0", tickprefix="$", tickformat=","),
            xaxis=dict(gridcolor="#f0f0f0"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── per-stock breakdown ───────────────────────────────────────────────
        st.markdown("---")
        st.subheader("Per-stock breakdown")
        for r in results:
            e    = r["entry"]
            res  = r["res"]
            info = r["info"]
            gain = res["final_value"] - res["invested"]
            gain_pct = (gain / res["invested"] * 100) if res["invested"] else 0
            period_label = f"{e['period_val']} {e['period_unit'].lower()}"
            col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
            col_a.markdown(f"**{e['ticker']}** — {info['name']}  \n"
                           f"<span style='font-size:0.78rem;color:#888'>{e['freq']} · {period_label} · {round(info['rate']*100)}% avg/yr</span>",
                           unsafe_allow_html=True)
            col_b.metric("Invested", f"${res['invested']:,.0f}")
            col_c.metric("Gain", f"+${gain:,.0f}", f"+{gain_pct:.1f}%")
            col_d.metric("Total", f"${res['final_value']:,.0f}")

        # ── scenarios ────────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("Bear / base / bull scenarios")
        b_inv, b_fin = calc_scenario(resolved, 0.5)
        ba_inv, ba_fin = calc_scenario(resolved, 1.0)
        bu_inv, bu_fin = calc_scenario(resolved, 1.5)

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown("#### 🐻 Bear case")
            st.markdown("Market underperforms. Half of expected returns.")
            st.metric("Final value", f"${b_fin:,.0f}", f"+${b_fin-b_inv:,.0f}")
        with sc2:
            st.markdown("#### 📊 Base case")
            st.markdown("Historical average returns. Most likely outcome.")
            st.metric("Final value", f"${ba_fin:,.0f}", f"+${ba_fin-ba_inv:,.0f}")
        with sc3:
            st.markdown("#### 🐂 Bull case")
            st.markdown("Strong AI cycle, rate cuts, outperformance.")
            st.metric("Final value", f"${bu_fin:,.0f}", f"+${bu_fin-bu_inv:,.0f}")

        st.caption(
            "⚠️ Projections use historical average annual returns with dividends reinvested. "
            "Bear / base / bull cases apply 0.5× / 1× / 1.5× variance. "
            "Not a guarantee of future performance. Not financial advice."
        )
