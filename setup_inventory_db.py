import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create the inventory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    SKU TEXT PRIMARY KEY,
    Name TEXT,
    Quantity INTEGER
)
""")

# Insert dummy products
sample_data = [
    ("SKU123", "Product A", 45),
    ("SKU456", "Product B", 30),
    ("SKU789", "Product C", 0)  # Out-of-stock example
]

for sku, name, qty in sample_data:
    cursor.execute("INSERT OR REPLACE INTO inventory (SKU, Name, Quantity) VALUES (?, ?, ?)", (sku, name, qty))

conn.commit()
conn.close()

print("✅ Fresh inventory database created.")
