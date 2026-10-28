
import pandas as pd

df = pd.read_excel("online_retail_raw_data.xlsx")

print("\nFIRST 5 ROWS OF THE DATASET:")
print(df.head())

print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nDATASET INFORMATION:")
df.info()

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nEXACT DUPLICATE ROWS:")
print(df.duplicated().sum())


print("\nCANCELLATION INVOICES:")
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print("Rows with cancellation invoice numbers:", cancelled.sum())

print("\nNEGATIVE QUANTITIES:")
negative_qty = df["Quantity"] < 0
print("Rows with negative quantities:", negative_qty.sum())
print(df.loc[negative_qty, [
    "InvoiceNo", "StockCode", "Quantity", "UnitPrice"
]].head(10))

print("\nZERO OR NEGATIVE UNIT PRICES:")
invalid_price = df["UnitPrice"] <= 0
print("Rows with UnitPrice <= 0:", invalid_price.sum())
print(df.loc[invalid_price, [
    "InvoiceNo", "StockCode", "Quantity", "UnitPrice"
]].head(10))

print("\nDUPLICATE ROW EXAMPLES:")
duplicates = df[df.duplicated(keep=False)]
print(duplicates.head(10))

print("\nMISSING CUSTOMER IDs:")
print("Rows without CustomerID:", df["CustomerID"].isna().sum())
print("Distinct invoices without CustomerID:",
      df.loc[df["CustomerID"].isna(), "InvoiceNo"].nunique())

print("\nMISSING PRODUCT DESCRIPTIONS:")
print("Rows without Description:", df["Description"].isna().sum())
print("Distinct stock codes without Description:",
      df.loc[df["Description"].isna(), "StockCode"].nunique())


print("\nCANCELLATION AND NEGATIVE QUANTITY OVERLAP:")

cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
negative_qty = df["Quantity"] < 0

print("Cancellation rows with negative quantity:",
      (cancelled & negative_qty).sum())

print("Negative-quantity rows without cancellation invoice number:",
      (~cancelled & negative_qty).sum())


print("\nUNIT PRICE BREAKDOWN:")

print("Zero unit prices:", (df["UnitPrice"] == 0).sum())
print("Negative unit prices:", (df["UnitPrice"] < 0).sum())


print("\nEXACT DUPLICATE BREAKDOWN AND FREQUENCY:")

duplicate_mask = df.duplicated(keep=False)
duplicate_groups = df[duplicate_mask].value_counts()

print("Rows belonging to duplicate groups:", duplicate_mask.sum())
print("Distinct duplicated row patterns:", len(duplicate_groups))
print("Extra copies beyond the first occurrence:",
      df.duplicated().sum())

print("\nMost frequently repeated exact rows:")
print(duplicate_groups.head(10))


print("\nNEGATIVE UNIT PRICE RECORDS DETAILS:")

print(
    df.loc[df["UnitPrice"] < 0, [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country"
    ]].to_string(index=True)
)


print("\nINSPECT REPEATED INVOICE 555524 DETAILS:")

invoice = df[df["InvoiceNo"].astype(str) == "555524"]

print("Number of rows in this invoice:", len(invoice))
print(invoice.to_string(index=True))


print("\nDUPLICATE ROW COUNTS FOR INVOICE 555524:")

print(
    invoice.value_counts().to_string()
)
