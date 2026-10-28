import pandas as pd

df = pd.read_excel("online_retail_raw_data.xlsx")

df.columns = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
    "country"
]

df["is_cancellation"] = (
    df["invoice_no"].astype(str).str.startswith("C")
)

df["is_negative_quantity"] = df["quantity"] < 0
df["is_zero_price"] = df["unit_price"] == 0
df["is_negative_price"] = df["unit_price"] < 0

df.insert(0, "source_row_id", range(1, len(df) + 1))

df.to_csv("online_retail_staging.csv", index=False)

print("Staging CSV created successfully.")
print("Rows saved:", len(df))
print("Columns saved:", len(df.columns))
print("Missing customer IDs:", df["customer_id"].isna().sum())
print("Exact duplicate source rows:", df.drop(
    columns=["source_row_id"]
).duplicated().sum())
