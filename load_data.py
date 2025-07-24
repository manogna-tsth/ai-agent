import pandas as pd
import sqlite3

# Step 1: Connect to SQLite database
print("Connecting to SQLite...")
conn = sqlite3.connect("ecommerce.db")

# Step 2: Load CSVs with debug messages
print("Reading CSV files...")

try:
    ad_sales = pd.read_csv("data/Product-Level Ad Sales and Metrics (mapped).csv")
    print("Loaded: Ad Sales")

    total_sales = pd.read_csv("data/Product-Level Total Sales and Metrics (mapped).csv")
    print("Loaded: Total Sales")

    eligibility = pd.read_csv("data/Product-Level Eligibility Table (mapped).csv")
    print("Loaded: Eligibility Table")
except Exception as e:
    print(" Error while reading CSVs:", e)
    conn.close()
    exit()

# Step 3: Save to SQL tables
print("Saving tables to database...")
try:
    ad_sales.to_sql("ad_sales_metrics", conn, if_exists="replace", index=False)
    total_sales.to_sql("total_sales_metrics", conn, if_exists="replace", index=False)
    eligibility.to_sql("eligibility_table", conn, if_exists="replace", index=False)
    print("All tables saved to database.")
except Exception as e:
    print("Error while saving to database:", e)
    conn.close()
    exit()

# Step 4: Close the connection
conn.close()
print("Done! Data successfully saved in ecommerce.db")

