
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 1. Dashboard configuration
# --------------------------------------------------

TEAL = "#0F766E"
TURQUOISE = "#14B8A6"
LIGHT_TURQUOISE = "#CCFBF1"
DARK_TEAL = "#134E4A"

st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. Dashboard header
# --------------------------------------------------

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #134E4A, #0F766E);
        padding: 24px 28px;
        border-radius: 14px;
        margin-bottom: 18px;
    ">
        <div style="
            color: #99F6E4;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 2px;
        ">
            SALES INTELLIGENCE
        </div>
        <div style="
            color: white;
            font-size: 30px;
            font-weight: 700;
            margin-top: 6px;
        ">
            Sales Performance Dashboard
        </div>
        <div style="
            color: #CCFBF1;
            font-size: 15px;
            margin-top: 8px;
        ">
            Explore revenue, profitability, product performance,
            and monthly sales trends.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 3. Dashboard styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #E6FFFA;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #134E4A !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        border: 1px solid #5EEAD4 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stMetric"] {
        background-color: #F0FDFA;
        border: 1px solid #99F6E4;
        padding: 10px 12px;
        border-radius: 10px;
    }

    div[data-testid="stMetricLabel"] p {
        color: #134E4A;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #0F766E;
        font-size: 1.35rem;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    h1 {
        font-size: 1.65rem !important;
    }

    h2, h3 {
        margin-top: 0.35rem !important;
        margin-bottom: 0.35rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# 4. Load and prepare dataset
# --------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv("data/superstore_full.csv")

    data["Order Date"] = pd.to_datetime(
        data["Order Date"],
        format="%d/%m/%y"
    )

    data["Ship Date"] = pd.to_datetime(
        data["Ship Date"],
        format="%d/%m/%y"
    )

    data["Order Month"] = (
        data["Order Date"].dt.to_period("M").astype(str)
    )

    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset not found. Please check that "
        "'data/superstore_full.csv' exists in your project folder."
    )
    st.stop()
except (KeyError, ValueError) as error:
    st.error(f"Please check the dataset columns and date formats: {error}")
    st.stop()

# --------------------------------------------------
# 5. Sidebar filters
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All Regions"] + sorted(df["Region"].dropna().unique().tolist())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All Categories"] + sorted(
        df["Category"].dropna().unique().tolist()
    )
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Order Date"].min().date(),
    min_value=df["Order Date"].min().date(),
    max_value=df["Order Date"].max().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Order Date"].max().date(),
    min_value=df["Order Date"].min().date(),
    max_value=df["Order Date"].max().date()
)

if start_date > end_date:
    st.error("Start Date cannot be later than End Date.")
    st.stop()

# --------------------------------------------------
# 6. Apply filters
# --------------------------------------------------

filtered_df = df[
    (df["Order Date"] >= pd.Timestamp(start_date)) &
    (df["Order Date"] < pd.Timestamp(end_date) + pd.Timedelta(days=1))
].copy()

if selected_region != "All Regions":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All Categories":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

st.markdown(
    f"""
    <div style="
        color: #064E4B;
        font-size: 15px;
        font-weight: 500;
        background-color: #CCFBF1;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 15px;
    ">
        Showing data from {start_date.strftime('%d %b %Y')}
        to {end_date.strftime('%d %b %Y')}
        | Region: {selected_region}
        | Category: {selected_category}
    </div>
    """,
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning(
        "No records match your selected filters. "
        "Please change the region, category, or date range."
    )
    st.stop()

# --------------------------------------------------
# 7. Calculate KPIs
# --------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

# Compare against the previous period of equal length
period_days = (end_date - start_date).days + 1

previous_start = (
    pd.Timestamp(start_date) - pd.Timedelta(days=period_days)
)

previous_df = df[
    (df["Order Date"] >= previous_start) &
    (df["Order Date"] < pd.Timestamp(start_date))
].copy()

if selected_region != "All Regions":
    previous_df = previous_df[
        previous_df["Region"] == selected_region
    ]

if selected_category != "All Categories":
    previous_df = previous_df[
        previous_df["Category"] == selected_category
    ]

previous_sales = previous_df["Sales"].sum()

if previous_sales > 0:
    sales_change_pct = (
        (total_sales - previous_sales) / previous_sales
    ) * 100
else:
    sales_change_pct = None

# --------------------------------------------------
# 8. KPI cards
# --------------------------------------------------

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5, gap="small")

with kpi1:
    st.metric("💰 Total Sales", f"${total_sales:,.2f}")

with kpi2:
    st.metric("📈 Total Profit", f"${total_profit:,.2f}")

with kpi3:
    st.metric("📦 Quantity Sold", f"{total_quantity:,.0f}")

with kpi4:
    st.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

with kpi5:
    if sales_change_pct is None:
        st.metric(
            "📉 Sales Change",
            "N/A",
            help="No positive previous-period sales available."
        )
    else:
        st.metric(
            "📉 Sales Change",
            f"{sales_change_pct:+.2f}%",
            delta=f"{sales_change_pct:+.2f}%",
            help="Compared with the previous period of equal length."
        )

st.divider()

# --------------------------------------------------
# 9. Sales by Category
# 10. Profit by Region
# --------------------------------------------------

chart_col1, chart_col2 = st.columns(2, gap="large")

with chart_col1:
    st.subheader("Sales by Category")

    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        text_auto=".2s",
        color="Category",
        color_discrete_sequence=[
            TEAL, TURQUOISE, "#5EEAD4"
        ],
        template="plotly_white"
    )

    fig_category.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig_category.update_layout(
        height=360,
        title="Sales by Category",
        title_font_color=DARK_TEAL,
        font=dict(color=DARK_TEAL),
        xaxis_title="Category",
        yaxis_title="Sales ($)",
        margin=dict(l=15, r=15, t=55, b=15),
        showlegend=False
    )

    fig_category.update_yaxes(
        tickprefix="$",
        separatethousands=True,
        gridcolor="#E2E8F0",
        zeroline=False
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with chart_col2:
    st.subheader("Profit by Region")

    region_profit = (
        filtered_df.groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    fig_region = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        text_auto=".2s",
        color="Region",
        color_discrete_sequence=[
            TEAL, TURQUOISE, "#5EEAD4", "#99F6E4"
        ],
        template="plotly_white"
    )

    fig_region.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig_region.update_layout(
        height=360,
        title="Profit by Region",
        title_font_color=DARK_TEAL,
        font=dict(color=DARK_TEAL),
        xaxis_title="Region",
        yaxis_title="Profit ($)",
        margin=dict(l=15, r=15, t=55, b=15),
        showlegend=False
    )

    fig_region.update_yaxes(
        tickprefix="$",
        separatethousands=True,
        gridcolor="#E2E8F0",
        zeroline=True,
        zerolinecolor="#94A3B8"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# --------------------------------------------------
# 11. Monthly Sales Trend — full dashboard width
# --------------------------------------------------

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby("Order Month", as_index=False)["Sales"]
    .sum()
    .sort_values("Order Month")
)

fig_monthly = px.line(
    monthly_sales,
    x="Order Month",
    y="Sales",
    markers=True,
    template="plotly_white",
    color_discrete_sequence=[TEAL],
    labels={
        "Order Month": "Month",
        "Sales": "Total Sales ($)"
    }
)

fig_monthly.update_traces(
    line=dict(width=3),
    marker=dict(
        color=TURQUOISE,
        size=7,
        line=dict(color="white", width=1)
    ),
    hovertemplate=(
        "Month: %{x}<br>"
        "Sales: $%{y:,.2f}"
        "<extra></extra>"
    )
)

fig_monthly.update_layout(
    height=400,
    font=dict(color=DARK_TEAL),
    margin=dict(l=20, r=20, t=25, b=20),
    hovermode="x unified"
)

fig_monthly.update_yaxes(
    tickprefix="$",
    separatethousands=True,
    gridcolor="#E2E8F0",
    zeroline=False
)

fig_monthly.update_xaxes(showgrid=False)

st.plotly_chart(
    fig_monthly,
    use_container_width=True,
    config={"displayModeBar": False}
)

# --------------------------------------------------
# 12. Year-over-Year Sales Comparison
# --------------------------------------------------

st.subheader("📅 Year-over-Year Sales Comparison")

yearly_sales = filtered_df.copy()
yearly_sales["Year"] = yearly_sales["Order Date"].dt.year

yearly_summary = (
    yearly_sales.groupby("Year", as_index=False)["Sales"]
    .sum()
    .sort_values("Year")
)

yearly_summary["Sales Growth (%)"] = (
    yearly_summary["Sales"].pct_change() * 100
)

yearly_summary["Year"] = yearly_summary["Year"].astype(str)

fig_yearly = px.bar(
    yearly_summary,
    x="Year",
    y="Sales",
    text="Sales",
    template="plotly_white",
    color_discrete_sequence=[TEAL],
    labels={
        "Year": "Year",
        "Sales": "Total Sales ($)"
    },
    hover_data={
        "Sales": ":$,.2f",
        "Sales Growth (%)": ":.2f"
    }
)

fig_yearly.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "Year: %{x}<br>"
        "Total Sales: $%{y:,.2f}"
        "<extra></extra>"
    )
)

fig_yearly.update_layout(
    height=420,
    showlegend=False,
    font=dict(color=DARK_TEAL),
    margin=dict(l=20, r=30, t=30, b=20),
    xaxis=dict(
        title="Year",
        type="category",
        showgrid=False
    ),
    yaxis=dict(
        title="Total Sales ($)",
        tickprefix="$",
        tickformat=",.0f",
        gridcolor="#E5E7EB",
        zeroline=False
    ),
    bargap=0.35
)

st.plotly_chart(
    fig_yearly,
    use_container_width=True,
    config={"displayModeBar": False}
)

# --------------------------------------------------
# 13. Annual Sales Growth Table
# --------------------------------------------------

st.subheader("📈 Annual Sales Growth")

growth_summary = yearly_summary.copy()

growth_summary["Sales"] = growth_summary["Sales"].map(
    lambda value: f"${value:,.2f}"
)

growth_summary["Sales Growth (%)"] = growth_summary[
    "Sales Growth (%)"
].map(
    lambda value: "N/A" if pd.isna(value) else f"{value:+.2f}%"
)

st.dataframe(
    growth_summary,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# 14. Top 10 Products by Sales
# --------------------------------------------------

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
    .sort_values("Sales", ascending=True)
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    text_auto=".2s",
    template="plotly_white",
    color_discrete_sequence=[TURQUOISE],
    labels={
        "Sales": "Sales ($)",
        "Product Name": "Product"
    }
)

fig_products.update_layout(
    height=450,
    font=dict(color=DARK_TEAL),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=20, t=25, b=10),
    showlegend=False
)

fig_products.update_xaxes(
    tickprefix="$",
    separatethousands=True,
    gridcolor="#E2E8F0"
)

st.plotly_chart(
    fig_products,
    use_container_width=True,
    config={"displayModeBar": False}
)

# --------------------------------------------------
# 15. Profit by Sub-Category
# --------------------------------------------------

st.subheader("💹 Profit by Sub-Category")

subcategory_profit = (
    filtered_df.groupby("Sub-Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=True)
)

fig_subcategory = px.bar(
    subcategory_profit,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    text_auto=".2s",
    template="plotly_white",
    color="Profit",
    color_continuous_scale=[
        "#F87171", "#CCFBF1", "#0F766E"
    ],
    color_continuous_midpoint=0,
    labels={
        "Profit": "Profit ($)",
        "Sub-Category": "Sub-Category"
    }
)

fig_subcategory.update_layout(
    height=500,
    font=dict(color=DARK_TEAL),
    margin=dict(l=10, r=10, t=25, b=10),
    coloraxis_showscale=False
)

fig_subcategory.update_xaxes(
    tickprefix="$",
    separatethousands=True,
    gridcolor="#E2E8F0",
    zeroline=True,
    zerolinecolor="#64748B"
)

st.plotly_chart(
    fig_subcategory,
    use_container_width=True,
    config={"displayModeBar": False}
)

# --------------------------------------------------
# 16. Business Insights
# --------------------------------------------------

st.subheader("💡 Business Insights")

profit_by_subcategory = (
    filtered_df.groupby("Sub-Category")["Profit"].sum()
)

sales_by_category = (
    filtered_df.groupby("Category")["Sales"].sum()
)

best_subcategory = profit_by_subcategory.idxmax()
best_profit = profit_by_subcategory.max()

worst_subcategory = profit_by_subcategory.idxmin()
worst_profit = profit_by_subcategory.min()

best_category = sales_by_category.idxmax()
best_category_sales = sales_by_category.max()

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(
        f"""
        <div style="
            background-color: #F0FDFA;
            border: 1px solid #99F6E4;
            border-radius: 12px;
            padding: 18px;
            min-height: 135px;
        ">
            <div style="color: #134E4A; font-size: 14px;">
                🏆 Most Profitable Sub-Category
            </div>
            <div style="
                color: #0F766E;
                font-size: 22px;
                font-weight: 700;
                margin-top: 10px;
            ">
                {best_subcategory}
            </div>
            <div style="color: #134E4A; font-size: 14px;">
                Profit: ${best_profit:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with insight2:
    st.markdown(
        f"""
        <div style="
            background-color: #F0FDFA;
            border: 1px solid #99F6E4;
            border-radius: 12px;
            padding: 18px;
            min-height: 135px;
        ">
            <div style="color: #134E4A; font-size: 14px;">
                📈 Top Sales Category
            </div>
            <div style="
                color: #0F766E;
                font-size: 22px;
                font-weight: 700;
                margin-top: 10px;
            ">
                {best_category}
            </div>
            <div style="color: #134E4A; font-size: 14px;">
                Sales: ${best_category_sales:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with insight3:
    st.markdown(
        f"""
        <div style="
            background-color: #FFF7F7;
            border: 1px solid #FECACA;
            border-radius: 12px;
            padding: 18px;
            min-height: 135px;
        ">
            <div style="color: #991B1B; font-size: 14px;">
                ⚠️ Lowest-Profit Sub-Category
            </div>
            <div style="
                color: #B91C1C;
                font-size: 22px;
                font-weight: 700;
                margin-top: 10px;
            ">
                {worst_subcategory}
            </div>
            <div style="color: #991B1B; font-size: 14px;">
                Profit: ${worst_profit:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# 17. Loss-Making Sub-Categories
# --------------------------------------------------

st.subheader("⚠️ Loss-Making Sub-Categories")

loss_subcategories = (
    subcategory_profit[
        subcategory_profit["Profit"] < 0
    ]
    .sort_values("Profit")
    .copy()
)

if loss_subcategories.empty:
    st.info(
        "No loss-making subcategories found for the selected filters."
    )
else:
    loss_subcategories["Profit"] = loss_subcategories["Profit"].map(
        lambda value: f"-${abs(value):,.2f}"
    )

    st.dataframe(
        loss_subcategories,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# 18. Download Filtered Data
# --------------------------------------------------

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data (CSV)",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# --------------------------------------------------
# 19. Dataset Preview
# --------------------------------------------------

st.subheader("🔎 Filtered Dataset Preview")

info1, info2 = st.columns(2)

with info1:
    st.metric("Filtered Records", f"{len(filtered_df):,}")

with info2:
    st.metric("Number of Columns", f"{len(filtered_df.columns):,}")

st.dataframe(
    filtered_df.head(10),
    use_container_width=True,
    hide_index=True
)
