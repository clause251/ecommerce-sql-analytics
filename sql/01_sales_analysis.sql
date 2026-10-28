-- 1. Overall sales performance
SELECT
    COUNT(DISTINCT invoice_no) AS total_invoices,
    COUNT(*) AS total_transaction_lines,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(quantity * unit_price), 2) AS total_sales
FROM invoice_items
WHERE is_cancellation = 0
  AND quantity > 0
  AND unit_price > 0;


-- 2. Monthly sales trend
SELECT
    strftime('%Y-%m', invoice_date) AS sales_month,
    ROUND(SUM(quantity * unit_price), 2) AS monthly_sales,
    COUNT(DISTINCT invoice_no) AS total_invoices
FROM invoice_items
WHERE is_cancellation = 0
  AND quantity > 0
  AND unit_price > 0
GROUP BY strftime('%Y-%m', invoice_date)
ORDER BY sales_month;


-- 3. Top 10 products by gross sales value
SELECT
    ii.stock_code,
    p.description,
    SUM(ii.quantity) AS units_sold,
    ROUND(SUM(ii.quantity * ii.unit_price), 2) AS gross_sales
FROM invoice_items AS ii
LEFT JOIN products AS p
    ON ii.stock_code = p.stock_code
WHERE ii.is_cancellation = 0
  AND ii.quantity > 0
  AND ii.unit_price > 0
GROUP BY ii.stock_code, p.description
ORDER BY gross_sales DESC
LIMIT 10;


-- 4. Top 10 countries by gross sales
SELECT
    c.country_name,
    COUNT(DISTINCT ii.invoice_no) AS total_invoices,
    ROUND(SUM(ii.quantity * ii.unit_price), 2) AS gross_sales
FROM invoice_items AS ii
JOIN invoices AS i
    ON ii.invoice_no = i.invoice_no
JOIN countries AS c
    ON i.country_id = c.country_id
WHERE ii.is_cancellation = 0
  AND ii.quantity > 0
  AND ii.unit_price > 0
GROUP BY c.country_name
ORDER BY gross_sales DESC
LIMIT 10;


-- 5. Top 10 customers by gross sales
SELECT
    ii_customer.customer_id,
    COUNT(DISTINCT ii_customer.invoice_no) AS total_invoices,
    ROUND(
        SUM(ii_customer.quantity * ii_customer.unit_price), 2
    ) AS gross_sales
FROM (
    SELECT
        ii.invoice_no,
        ii.quantity,
        ii.unit_price,
        i.customer_id
    FROM invoice_items AS ii
    JOIN invoices AS i
        ON ii.invoice_no = i.invoice_no
    WHERE ii.is_cancellation = 0
      AND ii.quantity > 0
      AND ii.unit_price > 0
      AND i.customer_id IS NOT NULL
) AS ii_customer
GROUP BY ii_customer.customer_id
ORDER BY gross_sales DESC
LIMIT 10;


-- 6. Top 3 products by sales in each month
WITH monthly_product_sales AS (
    SELECT
        strftime('%Y-%m', ii.invoice_date) AS sales_month,
        ii.stock_code,
        p.description,
        SUM(ii.quantity * ii.unit_price) AS gross_sales
    FROM invoice_items AS ii
    LEFT JOIN products AS p
        ON ii.stock_code = p.stock_code
    WHERE ii.is_cancellation = 0
      AND ii.quantity > 0
      AND ii.unit_price > 0
    GROUP BY
        strftime('%Y-%m', ii.invoice_date),
        ii.stock_code,
        p.description
),
ranked_products AS (
    SELECT
        sales_month,
        stock_code,
        description,
        ROUND(gross_sales, 2) AS gross_sales,
        ROW_NUMBER() OVER (
            PARTITION BY sales_month
            ORDER BY gross_sales DESC
        ) AS product_rank
    FROM monthly_product_sales
)
SELECT
    sales_month,
    stock_code,
    description,
    gross_sales,
    product_rank
FROM ranked_products
WHERE product_rank <= 3
ORDER BY sales_month, product_rank;


-- 7. Customer purchase frequency
WITH customer_orders AS (
    SELECT
        i.customer_id,
        COUNT(DISTINCT ii.invoice_no) AS total_invoices,
        ROUND(
            SUM(ii.quantity * ii.unit_price), 2
        ) AS gross_sales
    FROM invoice_items AS ii
    JOIN invoices AS i
        ON ii.invoice_no = i.invoice_no
    WHERE i.customer_id IS NOT NULL
      AND ii.is_cancellation = 0
      AND ii.quantity > 0
      AND ii.unit_price > 0
    GROUP BY i.customer_id
)
SELECT
    CASE
        WHEN total_invoices = 1 THEN 'One-time customer'
        ELSE 'Repeat customer'
    END AS customer_type,
    COUNT(*) AS number_of_customers,
    ROUND(SUM(gross_sales), 2) AS combined_gross_sales
FROM customer_orders
GROUP BY customer_type
ORDER BY number_of_customers DESC;


-- 8. Month-over-month sales growth
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', invoice_date) AS sales_month,
        SUM(quantity * unit_price) AS gross_sales
    FROM invoice_items
    WHERE is_cancellation = 0
      AND quantity > 0
      AND unit_price > 0
    GROUP BY strftime('%Y-%m', invoice_date)
),
sales_comparison AS (
    SELECT
        sales_month,
        gross_sales,
        LAG(gross_sales) OVER (
            ORDER BY sales_month
        ) AS previous_month_sales
    FROM monthly_sales
)
SELECT
    sales_month,
    ROUND(gross_sales, 2) AS gross_sales,
    ROUND(previous_month_sales, 2) AS previous_month_sales,
    ROUND(
        100.0 * (gross_sales - previous_month_sales)
        / NULLIF(previous_month_sales, 0),
        2
    ) AS growth_percentage
FROM sales_comparison
ORDER BY sales_month;
