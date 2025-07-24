import sqlite3

# Connect to the database
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Run a test query
print("Running test query...")
cursor.execute("SELECT * FROM ad_sales_metrics LIMIT 5")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

conn.close()
print("Query complete.")
