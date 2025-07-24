import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Check ad_sales_metrics
print(" ad_sales_metrics columns:")
cursor.execute("PRAGMA table_info(ad_sales_metrics)")
for row in cursor.fetchall():
    print(row[1])

print("\n total_sales_metrics columns:")
cursor.execute("PRAGMA table_info(total_sales_metrics)")
for row in cursor.fetchall():
    print(row[1])

conn.close()
