

import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard colour theme
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

##st.title("📊 Sales Performance Dashboard")


# Dashboard header
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
            text-transform: uppercase;
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

st.divider()

# Load the complete dataset
df = pd.read_csv("data/superstore_full.csv")

# Convert dates into datetime format
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d/%m/%y"
)



df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d/%m/%y"
)

# Create a month column from the order date
df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)

# Region filter in sidebar
st.sidebar.header("Dashboard Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All Regions"] + sorted(df["Region"].unique().tolist())
)

# Category filter in sidebar
selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All Categories"] + sorted(df["Category"].unique().tolist())
)

# Date range filter
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

# Apply the selected region filter
if selected_region == "All Regions":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Region"] == selected_region]

# Apply the selected date range
filtered_df = filtered_df[
    (filtered_df["Order Date"] >= pd.Timestamp(start_date)) &
    (filtered_df["Order Date"] <= pd.Timestamp(end_date))
]

# Apply the selected category filter
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


# Calculate key business metrics using the selected region

# Handle empty filter results
if filtered_df.empty:
    st.warning(
        "No records match your selected filters. "
        "Please change the region, category, or date range."
    )
    st.stop()

# Calculate key business metrics
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()

# Calculate profit margin
profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0
    else 0
)


# Compare sales with the previous period of equal length
period_days = (end_date - start_date).days + 1

previous_start = start_date - pd.Timedelta(days=period_days)
previous_end = start_date - pd.Timedelta(days=1)

previous_df = df[
    (df["Order Date"] >= pd.Timestamp(previous_start)) &
    (df["Order Date"] < pd.Timestamp(start_date))
]

# Apply the same region filter
if selected_region != "All Regions":
    previous_df = previous_df[
        previous_df["Region"] == selected_region
    ]

# Apply the same category filter
if selected_category != "All Categories":
    previous_df = previous_df[
        previous_df["Category"] == selected_category
    ]

previous_sales = previous_df["Sales"].sum()

# Calculate percentage change safely
if previous_sales != 0:
    sales_change_pct = (
        (total_sales - previous_sales) / previous_sales
    ) * 100
else:
    sales_change_pct = None





# Dashboard styling
st.markdown(
    """
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #E6FFFA;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #E6FFFA;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #134E4A !important;
    }

    /* Sidebar dropdowns */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        border: 1px solid #5EEAD4 !important;
        border-radius: 8px !important;
    }

    /* Compact KPI cards */
    div[data-testid="stMetric"] {
        background-color: #F0FDFA;
        border: 1px solid #99F6E4;
        padding: 8px 12px;
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

    /* Compact dashboard spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.65rem;
    }

    /* Compact headings and dividers */
    h1 {
        font-size: 1.65rem !important;
    }

    h2, h3 {
        margin-top: 0.35rem !important;
        margin-bottom: 0.35rem !important;
    }

    hr {
        margin-top: 0.4rem;
        margin-bottom: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Four KPI cards

# KPI cards - two rows for better readability

# First row: three KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"${total_sales:,.2f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit:,.2f}"
    )

with col3:
    st.metric(
        label="📦 Quantity Sold",
        value=f"{total_quantity:,.0f}"
    )

# Second row: two KPI cards
st.markdown("")

col4, col5 = st.columns(2)

with col4:
    st.metric(
        label="📊 Profit Margin",
        value=f"{profit_margin:.2f}%"
    )

with col5:
    if sales_change_pct is None:
        st.metric(
            label="📈 Sales Change",
            value="N/A",
            help="Previous period has no recorded sales."
        )
        st.caption("No previous-period data")
    else:
        st.metric(
            label="📈 Sales Change",
            value=f"{sales_change_pct:+.2f}%",
            delta=f"{sales_change_pct:+.2f}%",
            help="Compared with the previous period of equal length."
        )




st.divider()


# Sales by category
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader("Sales by Category")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
)

    
    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Sales by Category",
        text_auto=".2s",
        color_discrete_sequence=[TURQUOISE]
)



    
    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales ($)",
        title_font_color=DARK_TEAL,
        title_font_size=16,
        font_color=DARK_TEAL,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=45, b=10),
        showlegend=False
)


    st.plotly_chart(
    fig_category,
    use_container_width=True,
    config={"displayModeBar": False}
)


# Monthly sales trend
st.subheader("Monthly Sales Trend")




monthly_sales = (
    filtered_df.groupby("Order Month")["Sales"]
    .sum()
    .reset_index()
)

# Create the line chart

fig_monthly = px.line(
    monthly_sales,
    x="Order Month",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True,
    line_shape="linear"
)

fig_monthly.update_traces(
    line=dict(color=TEAL, width=3),
    marker=dict(color=TURQUOISE, size=6)
)



fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales ($)",
    title_font_color=DARK_TEAL,
    title_font_size=16,
    font_color=DARK_TEAL,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=10, t=45, b=10),
    showlegend=False
)


st.plotly_chart(
    fig_monthly,
    use_container_width=True,
    config={"displayModeBar": False}
)


# Profit by region
with chart_col2:
    st.subheader("Profit by Region")

    region_profit = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
)

    
    fig_region = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        title="Profit by Region",
        text_auto=".2s",
        color_discrete_sequence=[TEAL]
)



    
    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Profit ($)",
        title_font_color=DARK_TEAL,
        title_font_size=16,
        font_color=DARK_TEAL,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=45, b=10),
        showlegend=False
)


    st.plotly_chart(
    fig_region,
    use_container_width=True,
    config={"displayModeBar": False}
)
    

# Year-over-Year Sales Comparison
st.subheader("📅 Year-over-Year Sales Comparison")

yearly_sales = filtered_df.copy()

yearly_sales["Year"] = yearly_sales["Order Date"].dt.year

yearly_summary = (
    yearly_sales.groupby("Year")["Sales"]
    .sum()
    .reset_index()
)

yearly_summary["Year"] = yearly_summary["Year"].astype(str)

# Calculate year-over-year sales growth
yearly_summary["Sales Growth (%)"] = (
    yearly_summary["Sales"].pct_change() * 100
)

fig_yearly = px.bar(
    yearly_summary,
    x="Year",
    y="Sales",
    text="Sales",
    title="Annual Sales Performance",
    color="Sales",
    color_continuous_scale=["#CCFBF1", "#14B8A6", "#0F766E"]
)

fig_yearly.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig_yearly.update_layout(
    xaxis_title="Year",
    yaxis_title="Total Sales ($)",
    coloraxis_showscale=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#134E4A"),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_yearly,
    use_container_width=True,
    config={"displayModeBar": False}
)

# Display annual sales growth
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

# Top 10 Products by Sales
st.subheader("Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

# Create the Top 10 Products chart

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales",
    text_auto=".2s",
    color_discrete_sequence=[TURQUOISE]
)



fig_products.update_layout(
    xaxis_title="Sales ($)",
    yaxis_title="Product",
    title_font_color=DARK_TEAL,
    title_font_size=16,
    font_color=DARK_TEAL,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=10, t=45, b=10),
    yaxis={"categoryorder": "total ascending"},
    showlegend=False
)


st.plotly_chart(
    fig_products,
    use_container_width=True,
    config={"displayModeBar": False}
)


# Profit by Sub-Category
st.subheader("Profit by Sub-Category")

subcategory_profit = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Profit", ascending=True)
)
# Create the Profit by Sub-Category chart

fig_subcategory = px.bar(
    subcategory_profit,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    title="Profit by Sub-Category",
    text_auto=".2s",
    color="Profit",
    color_continuous_scale=["#F87171", "#CCFBF1", "#0F766E"],
    color_continuous_midpoint=0
)



fig_subcategory.update_layout(
    xaxis_title="Profit ($)",
    yaxis_title="Sub-Category",
    title_font_color=DARK_TEAL,
    title_font_size=16,
    font_color=DARK_TEAL,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=10, t=45, b=10),
    showlegend=False
)


st.plotly_chart(
    fig_subcategory,
    use_container_width=True,
    config={"displayModeBar": False}
)



# Business Insights
st.subheader("💡 Business Insights")

if not filtered_df.empty:
    # Calculate profit by sub-category
    profit_by_subcategory = (
        filtered_df.groupby("Sub-Category")["Profit"].sum()
    )

    best_subcategory = profit_by_subcategory.idxmax()
    best_profit = profit_by_subcategory.max()

    worst_subcategory = profit_by_subcategory.idxmin()
    worst_profit = profit_by_subcategory.min()

    # Calculate sales by category
    sales_by_category = (
        filtered_df.groupby("Category")["Sales"].sum()
    )

    best_category = sales_by_category.idxmax()
    best_category_sales = sales_by_category.max()

    # Display insights in three columns
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
                <div style="color: #0F766E; font-size: 22px;
                            font-weight: 700; margin-top: 10px;">
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
                <div style="color: #0F766E; font-size: 22px;
                            font-weight: 700; margin-top: 10px;">
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
                <div style="color: #B91C1C; font-size: 22px;
                            font-weight: 700; margin-top: 10px;">
                    {worst_subcategory}
                </div>
                <div style="color: #991B1B; font-size: 14px;">
                    Profit: ${worst_profit:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.warning("No data available for the selected filters.")





# Identify loss-making subcategories
st.subheader("⚠️ Loss-Making Sub-Categories")

loss_subcategories = (
    subcategory_profit[subcategory_profit["Profit"] < 0]
    .sort_values("Profit")
    .copy()
)

if loss_subcategories.empty:
    st.info("No loss-making subcategories found for the selected filters.")
else:
    loss_subcategories["Profit"] = loss_subcategories["Profit"].map(
        lambda value: f"-${abs(value):,.2f}"
    )

    st.dataframe(
        loss_subcategories,
        use_container_width=True,
        hide_index=True
    )



# Download filtered data
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
# Display dataset information
st.subheader("Filtered Dataset Preview")

st.write("Number of filtered records:", len(filtered_df))
st.write("Number of columns:", len(filtered_df.columns))

st.dataframe(
    filtered_df.head(10),
    use_container_width=True
)


