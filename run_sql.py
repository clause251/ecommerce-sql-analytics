import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

with open("sql/01_sales_analysis.sql", "r") as file:
    sql_code = file.read()

queries = sql_code.split(";")

for query in queries:
    if query.strip():
        cursor.execute(query)
        print("\nQuery result:")
        for row in cursor.fetchall():
            print(row)

conn.close()