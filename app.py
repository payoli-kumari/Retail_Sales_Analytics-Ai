"""Streamlit Dashboard: streamlit run app.py"""
import re
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    layout="wide",
    page_icon="🛒",
    initial_sidebar_state="expanded",
)
ROOT = Path(__file__).resolve().parent


@st.cache_data
def load():
    return pd.read_csv(ROOT / "data" / "processed" / "clean_sales.csv",
                       parse_dates=["order_date", "ship_date"])


def has_hindi(text: str) -> bool:
    """Return True if the text contains Hindi (Devanagari) characters."""
    return bool(re.search(r"[\u0900-\u097F]", text))


df = load()

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS for a premium look
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e3a5f 0%, #16213e 100%);
        border: 1px solid #0f4c81;
        border-radius: 12px;
        padding: 16px 20px;
        color: white;
    }
    [data-testid="stMetricLabel"] { color: #8fb3e8 !important; font-size: 13px; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 26px; font-weight: 700; }
    [data-testid="stMetricDelta"] { color: #4ade80 !important; }
    .sidebar-title { font-size: 18px; font-weight: 700; color: #1e3a5f; margin-bottom: 4px; }
    div[data-testid="stSidebarContent"] { background: #f8faff; }
</style>
""", unsafe_allow_html=True)

st.title("🛒 Retail Sales Analytics Dashboard")
st.caption("Global Superstore · 2011–2014 · Powered by Python + Streamlit + AI")

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar Filters
# ──────────────────────────────────────────────────────────────────────────────
st.sidebar.header("🎛️ Dashboard Filters")

with st.sidebar.expander("📅 Time Filters", expanded=True):
    years = st.multiselect(
        "Year", sorted(df["year"].unique()),
        default=sorted(df["year"].unique()), key="year_filter"
    )
    quarters = st.multiselect(
        "Quarter", sorted(df["quarter"].unique()),
        default=sorted(df["quarter"].unique()), key="quarter_filter"
    )

with st.sidebar.expander("🌍 Geography & Segment", expanded=True):
    regions = st.multiselect(
        "Region", sorted(df["region"].unique()),
        default=sorted(df["region"].unique()), key="region_filter"
    )
    segments = st.multiselect(
        "Customer Segment", sorted(df["segment"].unique()),
        default=sorted(df["segment"].unique()), key="segment_filter"
    )

with st.sidebar.expander("📦 Product & Shipping", expanded=True):
    cats = st.multiselect(
        "Category", sorted(df["category"].unique()),
        default=sorted(df["category"].unique()), key="cat_filter"
    )
    ship_modes = st.multiselect(
        "Ship Mode", sorted(df["ship_mode"].unique()),
        default=sorted(df["ship_mode"].unique()), key="ship_filter"
    )

# Apply all filters
f = df[
    df["year"].isin(years) &
    df["quarter"].isin(quarters) &
    df["region"].isin(regions) &
    df["segment"].isin(segments) &
    df["category"].isin(cats) &
    df["ship_mode"].isin(ship_modes)
]

# Sidebar summary
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered rows:** {len(f):,} / {len(df):,}")
st.sidebar.markdown(f"**Orders:** {f['order_id'].nunique():,}")

# ──────────────────────────────────────────────────────────────────────────────
# Tabs
# ──────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🏆 Deep Analysis",
    "🤖 Ask the Data",
    "📚 Ask the Project (RAG)",
    "💡 AI Insights"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: Main Dashboard
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    if f.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your selection.")
        st.stop()

    # ── KPI Cards ────────────────────────────────────────────────────────────
    st.subheader("📌 Key Performance Indicators")
    c1, c2, c3, c4, c5 = st.columns(5)
    total_sales = f["sales"].sum()
    total_profit = f["profit"].sum()
    profit_margin = total_profit / total_sales * 100 if total_sales else 0
    total_orders = f["order_id"].nunique()
    avg_order_val = f.groupby("order_id")["sales"].sum().mean()

    c1.metric("💰 Total Sales", f"${total_sales:,.0f}")
    c2.metric("📈 Total Profit", f"${total_profit:,.0f}")
    c3.metric("🎯 Profit Margin", f"{profit_margin:.1f}%")
    c4.metric("📦 Orders", f"{total_orders:,}")
    c5.metric("🛍️ Avg Order Value", f"${avg_order_val:,.0f}")

    st.markdown("---")

    # ── Row 1: Trend + Category ───────────────────────────────────────────────
    col1, col2 = st.columns(2)

    trend = f.groupby("year_month", as_index=False)["sales"].sum()
    col1.plotly_chart(
        px.line(trend, x="year_month", y="sales",
                title="📅 Monthly Sales Trend",
                labels={"year_month": "Month", "sales": "Sales ($)"},
                color_discrete_sequence=["#0f4c81"],
                template="plotly_white")
        .update_traces(line_width=2.5),
        use_container_width=True
    )

    cat = f.groupby("category", as_index=False)[["sales", "profit"]].sum()
    col2.plotly_chart(
        px.bar(cat, x="category", y=["sales", "profit"],
               barmode="group", title="🏷️ Category: Sales vs Profit",
               labels={"value": "Amount ($)", "variable": "Metric"},
               color_discrete_map={"sales": "#0f4c81", "profit": "#10b981"},
               template="plotly_white"),
        use_container_width=True
    )

    # ── Row 2: Region + Discount ──────────────────────────────────────────────
    col3, col4 = st.columns(2)

    reg = f.groupby("region", as_index=False)["sales"].sum()
    col3.plotly_chart(
        px.pie(reg, names="region", values="sales",
               title="🌍 Sales by Region",
               color_discrete_sequence=px.colors.qualitative.Set2,
               template="plotly_white")
        .update_traces(textposition="inside", textinfo="percent+label"),
        use_container_width=True
    )

    sample = f.sample(min(1500, len(f)), random_state=1)
    col4.plotly_chart(
        px.scatter(sample, x="discount", y="profit",
                   color="category", opacity=0.55,
                   title="🔻 Discount vs Profit",
                   labels={"discount": "Discount Rate", "profit": "Profit ($)"},
                   color_discrete_sequence=px.colors.qualitative.Set2,
                   template="plotly_white"),
        use_container_width=True
    )

    # ── Data Table ────────────────────────────────────────────────────────────
    with st.expander("📋 View / Download Filtered Data"):
        st.dataframe(
            f[["order_id", "order_date", "region", "segment", "category",
               "sub_category", "product_name", "sales", "profit",
               "discount", "ship_mode"]].head(300),
            use_container_width=True
        )
        st.download_button(
            "⬇️ Download Filtered Data (CSV)",
            f.to_csv(index=False),
            "filtered_sales.csv",
            "text/csv"
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: Deep Analysis
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if f.empty:
        st.warning("⚠️ No data for the selected filters.")
        st.stop()

    st.subheader("🏆 Deep Dive Analysis")

    # ── Row 1: Sub-category + Segment ────────────────────────────────────────
    col1, col2 = st.columns(2)

    top_sub = (f.groupby("sub_category", as_index=False)["profit"].sum()
               .sort_values("profit", ascending=True).tail(15))
    col1.plotly_chart(
        px.bar(top_sub, x="profit", y="sub_category", orientation="h",
               title="📊 Sub-Category Profit Ranking",
               labels={"profit": "Total Profit ($)", "sub_category": "Sub-Category"},
               color="profit",
               color_continuous_scale=["#ef4444", "#f97316", "#10b981"],
               template="plotly_white"),
        use_container_width=True
    )

    seg = f.groupby("segment", as_index=False)[["sales", "profit"]].sum()
    col2.plotly_chart(
        px.bar(seg, x="segment", y=["sales", "profit"],
               barmode="group", title="👥 Segment: Sales vs Profit",
               labels={"value": "Amount ($)", "variable": "Metric"},
               color_discrete_map={"sales": "#6366f1", "profit": "#10b981"},
               template="plotly_white"),
        use_container_width=True
    )

    # ── Row 2: Ship Mode + Quarterly Trend ───────────────────────────────────
    col3, col4 = st.columns(2)

    ship = f.groupby("ship_mode", as_index=False)[["sales", "profit"]].sum()
    col3.plotly_chart(
        px.bar(ship, x="ship_mode", y="sales",
               title="🚚 Sales by Ship Mode",
               color="ship_mode",
               color_discrete_sequence=px.colors.qualitative.Pastel,
               template="plotly_white",
               labels={"sales": "Total Sales ($)", "ship_mode": "Ship Mode"}),
        use_container_width=True
    )

    q_trend = f.groupby(["year", "quarter"], as_index=False)["sales"].sum()
    q_trend["period"] = q_trend["year"].astype(str) + " Q" + q_trend["quarter"].astype(str)
    col4.plotly_chart(
        px.bar(q_trend, x="period", y="sales",
               title="📆 Quarterly Sales Trend",
               color="sales",
               color_continuous_scale="Blues",
               template="plotly_white",
               labels={"sales": "Sales ($)", "period": "Quarter"}),
        use_container_width=True
    )

    # ── Row 3: Discount impact + Top products ────────────────────────────────
    col5, col6 = st.columns(2)

    f2 = f.copy()
    f2["discount_band"] = pd.cut(
        f2["discount"], [-0.01, 0, 0.1, 0.2, 0.4, 1],
        labels=["0%", "1–10%", "11–20%", "21–40%", "40%+"]
    )
    disc = f2.groupby("discount_band", observed=True, as_index=False)[["sales", "profit"]].sum()
    disc["margin_%"] = (disc["profit"] / disc["sales"] * 100).round(1)
    col5.plotly_chart(
        px.bar(disc, x="discount_band", y="margin_%",
               title="🏷️ Profit Margin by Discount Band",
               labels={"discount_band": "Discount Band", "margin_%": "Margin (%)"},
               color="margin_%",
               color_continuous_scale=["#ef4444", "#f97316", "#10b981"],
               template="plotly_white"),
        use_container_width=True
    )

    top10 = (f.groupby("product_name", as_index=False)["sales"].sum()
             .sort_values("sales", ascending=False).head(10))
    col6.plotly_chart(
        px.bar(top10, x="sales", y="product_name", orientation="h",
               title="🥇 Top 10 Products by Sales",
               labels={"sales": "Total Sales ($)", "product_name": "Product"},
               color="sales",
               color_continuous_scale="Blues",
               template="plotly_white"),
        use_container_width=True
    )

    # ── Yearly Growth Table ───────────────────────────────────────────────────
    st.markdown("#### 📅 Yearly Sales & Profit Summary")
    yearly = (f.groupby("year")[["sales", "profit"]].sum()
              .assign(margin_pct=lambda d: d["profit"] / d["sales"] * 100)
              .round(2))
    yearly["growth_%"] = yearly["sales"].pct_change().mul(100).round(1)
    st.dataframe(yearly.style.format({
        "sales": "${:,.0f}", "profit": "${:,.0f}",
        "margin_pct": "{:.1f}%", "growth_%": "{:.1f}%"
    }), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: Ask the Data (AI)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🤖 Ask the Data")
    st.info("Ask any question about the **filtered data** — the AI writes pandas code and runs it for you.")
    q = st.text_input("💬 Your Question", placeholder="Which region has the highest profit margin?",
                      key="data_q")
    if st.button("🔍 Ask Data", key="ask_data_btn") and q:
        if has_hindi(q):
            st.warning("Please ask your question in English.")
            st.stop()
        try:
            from ai_chat import ask_data
            with st.spinner("🤔 Thinking..."):
                answer, code, result = ask_data(q, f)
            st.success(answer)
            with st.expander("🔬 Generated Code (for verification)"):
                st.code(code, language="python")
            if result is not None:
                st.write(result)
        except Exception as e:
            st.error(f"⚠️ Check AI setup (API key / LLM_PROVIDER in .env): {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: Ask the Project (RAG)
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📚 Ask the Project (RAG)")
    st.info("Answers come **only from the project documents** (data dictionary, analysis notes). Not affected by sidebar filters.")
    q2 = st.text_input("💬 Project Question",
                       placeholder="What was done in data cleaning? What is RFM?",
                       key="rag_q")
    if st.button("🔍 Ask Project", key="ask_rag_btn") and q2:
        if has_hindi(q2):
            st.warning("Please ask your question in English.")
            st.stop()
        try:
            from rag_chat import ask_project
            with st.spinner("🔎 Searching documents..."):
                ans, ctx = ask_project(q2)
            st.success(ans)
            if ans.strip().lower().startswith("not found"):
                st.info("💡 Tip: For numbers from the data, use the 'Ask the Data' tab.")
            with st.expander("📄 Sources used for this answer"):
                st.text(ctx)
        except Exception as e:
            st.error(f"⚠️ Check AI setup: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: AI Insights
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("💡 AI-Generated Business Insights")
    st.info("Click the button to generate 5 key insights + 3 business recommendations from the **filtered data**.")
    if st.button("✨ Generate AI Insights", key="ai_insights_btn"):
        if f.empty:
            st.warning("No data for the selected filters.")
        else:
            by_cat = f.groupby("category")[["sales", "profit"]].sum()
            by_reg = f.groupby("region")[["sales", "profit"]].sum()
            by_seg = f.groupby("segment")[["sales", "profit"]].sum()

            cat_sales_rank = " > ".join(by_cat["sales"].sort_values(ascending=False).index)
            cat_profit_rank = " > ".join(by_cat["profit"].sort_values(ascending=False).index)
            reg_sales_rank = " > ".join(by_reg["sales"].sort_values(ascending=False).index[:5])
            seg_rank = " > ".join(by_seg["sales"].sort_values(ascending=False).index)

            rules = (
                "RULES: Use only the facts below. Do not compare numbers yourself; "
                "use the rankings given. Do not invent causes. "
                "The loss-making percentage is about order lines, never say 'orders'.\n\n"
            )
            summary = rules + (
                f"Total sales {f['sales'].sum():,.0f}, profit {f['profit'].sum():,.0f}, "
                f"margin {f['profit'].sum()/f['sales'].sum()*100:.1f}%.\n"
                f"Orders: {f['order_id'].nunique():,}, Avg order value: {f.groupby('order_id')['sales'].sum().mean():,.0f}.\n"
                f"Categories ranked by sales (highest first): {cat_sales_rank}.\n"
                f"Categories ranked by profit (highest first): {cat_profit_rank}.\n"
                f"Top 5 regions ranked by sales: {reg_sales_rank}.\n"
                f"Highest-profit region: {by_reg['profit'].idxmax()}.\n"
                f"Segments ranked by sales: {seg_rank}.\n"
                f"By category:\n{by_cat.round(0)}\n"
                f"By region:\n{by_reg.round(0)}\n"
                f"Avg discount {f['discount'].mean():.2f}, "
                f"loss-making order lines {f['is_loss'].mean()*100:.1f}%."
            )
            try:
                from ai_chat import auto_insights
                with st.spinner("🤖 Generating insights..."):
                    st.markdown(auto_insights(summary))
            except Exception as e:
                st.error(f"⚠️ Check AI setup: {e}")