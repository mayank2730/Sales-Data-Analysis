# Sales Data Analysis Dashboard

An end-to-end sales analytics project built using Python, SQL, Streamlit, and Plotly. The project explores retail sales data to identify sales trends, evaluate profitability, compare yearly performance, and highlight loss-making product sub-categories through an interactive dashboard.

## Project Overview

This project uses the Sample Superstore dataset to analyze sales performance across different years, regions, product categories, and sub-categories.

The interactive dashboard allows users to filter data, monitor key performance indicators, explore charts, and download filtered records for further analysis.

## Features

- **Interactive filters:** Filter results by region, product category, and order date.
- **Key Performance Indicators:** Track total sales, total profit, quantity sold, and profit margin.
- **Sales trend analysis:** Explore monthly sales and annual sales performance.
- **Year-over-year analysis:** Compare yearly sales and calculate percentage growth.
- **Product analysis:** Identify top-selling products and compare sub-category profitability.
- **Business insights:** Highlight the most profitable sub-category, top sales category, and lowest-profit sub-category.
- **Loss analysis:** Identify sub-categories generating negative profit.
- **SQL analysis:** Use SQL queries to summarize sales, profitability, regional performance, and profit margins.
- **Data export:** Download filtered records as a CSV file.

## Technologies Used

- Python
- Pandas
- NumPy
- SQL and SQLite
- Streamlit
- Plotly
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Structure

```text
Sales-Data-Analysis/
├── dashboard/
│   └── app.py
├── data/
│   ├── superstore.csv
│   ├── superstore_full.csv
│   ├── category_profit.csv
│   ├── region_summary.csv
│   ├── monthly_summary.csv
│   └── sales.db
├── notebooks/
│   └── 01_sales_exploration.ipynb
├── sql/
│   └── sales_analysis.sql
├── README.md
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Sales-Data-Analysis
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

From the project root directory, run:

```bash
python -m streamlit run dashboard/app.py
```

Streamlit will open the dashboard in your browser.


# Sales Data Analysis Dashboard

An interactive sales analytics dashboard built using Python and Streamlit to explore sales performance, profit, product categories, and business trends.

## 🚀 Live Dashboard

**[Click here to view the live Sales Data Analysis Dashboard](https://sales-data-analysis-pq3hduvssxxpflkzqkzwfg.streamlit.app/)**

## 💻 GitHub Repository

[View the source code](https://github.com/mayank2730/Sales-Data-Analysis)

## 🛠️ Technologies Used

- Python
- Pandas
- Streamlit
- Data Visualization

## ✨ Key Features

- Interactive sales data analysis
- Sales and profit performance tracking
- Category and product-level insights
- Visual exploration of business trends

## ⚙️ Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/mayank2730/Sales-Data-Analysis.git
   ```

2. Navigate to the project folder:

   ```bash
   cd Sales-Data-Analysis
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```


## SQL Analysis

The SQL script in `sql/sales_analysis.sql` includes queries for:

- Overall sales and profit
- Profit by product category
- Sales by region
- Loss-making sub-categories
- Profit margin by category

## Key Findings

The analysis of the included Superstore dataset identified the following patterns:

- Technology was the highest-sales product category in the overall dataset.
- The West region generated the highest total profit.
- Tables, Bookcases, and Supplies recorded negative total profit in the overall dataset.
- Annual sales increased substantially in 2016 and 2017 compared with 2015.

These findings refer to the overall dataset; dashboard results may change when filters are applied.

## Learning Outcomes

Through this project, I practiced data cleaning, exploratory data analysis, SQL querying, KPI calculations, data visualization, and interactive dashboard development.

## Future Improvements

- Add sales forecasting.
- Introduce customer segmentation.
- Deploy the dashboard online.
- Expand the analysis with additional business metrics.

## Author

**Mayank Raj**

