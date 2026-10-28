import sqlite3

conn = sqlite3.connect("ecommerce.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS invoice_items;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY
);

CREATE TABLE countries (
    country_id INTEGER PRIMARY KEY,
    country_name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    stock_code TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE invoices (
    invoice_no TEXT PRIMARY KEY,
    customer_id INTEGER,
    country_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

CREATE TABLE invoice_items (
    source_row_id INTEGER PRIMARY KEY,
    invoice_no TEXT NOT NULL,
    stock_code TEXT,
    description TEXT,
    invoice_date TEXT,
    quantity INTEGER,
    unit_price REAL,
    is_cancellation INTEGER,
    is_negative_quantity INTEGER,
    is_zero_price INTEGER,
    is_negative_price INTEGER,
    FOREIGN KEY (invoice_no) REFERENCES invoices(invoice_no),
    FOREIGN KEY (stock_code) REFERENCES products(stock_code)
);
""")

cursor.execute("""
INSERT INTO customers (customer_id)
SELECT DISTINCT CAST(customer_id AS INTEGER)
FROM raw_online_retail
WHERE customer_id IS NOT NULL
""")

cursor.execute("""
INSERT INTO countries (country_name)
SELECT DISTINCT country
FROM raw_online_retail
WHERE country IS NOT NULL
""")

cursor.execute("""
INSERT INTO invoices (invoice_no, customer_id, country_id)
SELECT
    r.invoice_no,
    CAST(MAX(r.customer_id) AS INTEGER),
    c.country_id
FROM raw_online_retail AS r
JOIN countries AS c ON c.country_name = r.country
GROUP BY r.invoice_no
""")

cursor.execute("""
WITH description_counts AS (
    SELECT
        stock_code,
        TRIM(description) AS description,
        COUNT(*) AS frequency
    FROM raw_online_retail
    WHERE stock_code IS NOT NULL
      AND description IS NOT NULL
      AND LOWER(TRIM(description)) NOT IN (
          'damaged', 'damages', 'found', 'missing', '?missing',
          'adjustment', 're-adjustment', 'thrown away',
          'unsaleable, destroyed.', 'ebay'
      )
      AND LOWER(TRIM(description)) NOT LIKE 'wrongly%'
      AND LOWER(TRIM(description)) NOT LIKE 'marked as%'
    GROUP BY stock_code, TRIM(description)
),
ranked AS (
    SELECT
        stock_code,
        description,
        ROW_NUMBER() OVER (
            PARTITION BY stock_code
            ORDER BY frequency DESC, description
        ) AS rn
    FROM description_counts
)
INSERT INTO products (stock_code, description)
SELECT stock_code, description
FROM ranked
WHERE rn = 1
""")

cursor.execute("""
INSERT OR IGNORE INTO products (stock_code, description)
SELECT DISTINCT stock_code, NULL
FROM raw_online_retail
WHERE stock_code IS NOT NULL
""")

cursor.execute("""
INSERT INTO invoice_items (
    source_row_id, invoice_no, stock_code, description,
    invoice_date, quantity, unit_price,
    is_cancellation, is_negative_quantity,
    is_zero_price, is_negative_price
)
SELECT
    source_row_id, invoice_no, stock_code, description,
    invoice_date, quantity, unit_price,
    is_cancellation, is_negative_quantity,
    is_zero_price, is_negative_price
FROM raw_online_retail
""")

conn.commit()

print("Normalized tables created successfully.")

for table in (
    "customers", "countries", "products",
    "invoices", "invoice_items"
):
    count = cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    print(f"{table}: {count:,} rows")

print(
    "Foreign-key violations:",
    len(cursor.execute("PRAGMA foreign_key_check").fetchall())
)

conn.close()
