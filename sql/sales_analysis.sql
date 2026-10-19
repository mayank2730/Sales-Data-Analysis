
-- 1. Total sales and profit
SELECT
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore;


-- 2. Profit by category
SELECT
    Category,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY Category
ORDER BY total_profit DESC;


-- 3. Sales by region
SELECT
    Region,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY Region
ORDER BY total_sales DESC;


-- 4. Loss-making sub-categories
SELECT
    Sub_Category,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY Sub_Category
HAVING SUM(Profit) < 0
ORDER BY total_profit ASC;


-- 5. Profit margin by category
SELECT
    Category,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2)
        AS profit_margin_pct
FROM superstore
GROUP BY Category
ORDER BY profit_margin_pct DESC;
