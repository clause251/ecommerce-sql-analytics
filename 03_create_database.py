import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

df = pd.read_csv(
    "online_retail_staging.csv",
    parse_dates=["invoice_date"]
)

df.to_sql(
    "raw_online_retail",
    conn,
    if_exists="replace",
    index=False
)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM raw_online_retail")
row_count = cursor.fetchone()[0]

print("Database created: ecommerce.db")
print("Raw table created: raw_online_retail")
print("Rows loaded:", row_count)

cursor.execute("PRAGMA table_info(raw_online_retail)")

print("\nRAW TABLE COLUMNS:")
for column in cursor.fetchall():
    print(column)

conn.close()
