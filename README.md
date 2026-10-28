# E-commerce Sales Analytics Using SQL

## Project Overview

This project analyzes an online retail transaction dataset using SQL and SQLite to identify sales trends, top-performing products, important markets, and customer purchasing behavior.

The goal is to transform raw transaction data into meaningful business insights that can support data-driven decisions.

## Dataset

- **Source:** [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- **Original records:** 541,909 transaction lines
- **Period:** December 2010 to December 2011
- **Key fields:** Invoice number, product code, quantity, invoice date, unit price, customer ID, and country.

## Tools and Technologies

- SQL
- SQLite
- Python
- pandas
- Git and GitHub

## Database Design

The database contains a raw source table and five normalized tables:

- `raw_online_retail` — original imported transaction data
- `customers` — known customer IDs
- `countries` — country reference data
- `products` — product codes and selected descriptions
- `invoices` — invoice-level customer and country information
- `invoice_items` — transaction-level details

The normalized tables preserve all 541,909 transaction rows in `invoice_items`. Foreign-key validation returned zero violations.

## Business Questions Analyzed

1. What are the overall sales and transaction volumes?
2. How do sales change month by month?
3. Which products generate the highest gross sales?
4. Which countries contribute the most gross sales?
5. Which customers generate the highest gross sales?
6. Which products rank highest in sales within each month?
7. How do one-time and repeat customers compare?
8. What is the month-over-month sales growth?

## Key Findings

- Preliminary gross sales were £10,666,684.54 under the project's initial transaction filters.
- November 2011 had the highest monthly gross sales, at £1,509,496.33.
- The United Kingdom was the largest market in the country analysis, with £9,025,222.08 in gross sales.
- Customer 14646 ranked highest among identified customers, with £280,206.02 in gross sales.
- The customer analysis identified 2,845 repeat customers and 1,493 one-time customers.
- Sales growth varied throughout the period, with strong increases in September and November 2011.

## SQL Skills Demonstrated

- Filtering with `WHERE`
- Aggregation using `SUM`, `COUNT`, and `ROUND`
- Grouping with `GROUP BY`
- Sorting and limiting results
- Joining related tables
- Common Table Expressions (CTEs)
- Window functions such as `ROW_NUMBER()` and `LAG()`
- Conditional logic using `CASE`
- Month-level sales analysis and percentage growth calculations

## Data Quality and Limitations

- Customer IDs are missing from a portion of the source data, so customer-level analysis covers only identifiable customers.
- Cancellation invoices, non-positive quantities, and non-positive unit prices are excluded from the initial sales calculations.
- Product rankings may include postage, fees, and adjustment-related codes; therefore, they should not be interpreted as a clean ranking of physical merchandise.
- Gross sales are preliminary analytical measures, not audited net revenue or profit.
- The final month may have incomplete data coverage.

## Project Structure

- `01_inspect_data.py` — initial data inspection
- `02_prepare_data.py` — data preparation
- `03_create_database.py` — SQLite database creation
- `04_create_normalized_tables.py` — normalized table creation
- `run_sql.py` — executes the SQL analysis file
- `sql/01_sales_analysis.sql` — eight business analysis queries

## Future Improvements

- Build an interactive sales dashboard.
- Separate physical merchandise from service and adjustment codes.
- Improve return and cancellation handling.
- Add customer segmentation and more detailed retention analysis.
- Publish selected charts and documented insights.

