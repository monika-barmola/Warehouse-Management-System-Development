import sqlite3

# ========== DATABASE SETUP ==========
def create_table():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create the inventory table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            sku TEXT PRIMARY KEY,
            product_name TEXT,
            quantity INTEGER
        )
    ''')

    conn.commit()
    conn.close()


# ========== ADD PRODUCT ==========
def add_product(sku, product_name, quantity):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO inventory (sku, product_name, quantity) VALUES (?, ?, ?)",
                       (sku, product_name, quantity))
        conn.commit()
        print(f"✅ Product '{product_name}' added with quantity {quantity}.")
    except sqlite3.IntegrityError:
        print("❌ SKU already exists. Use update_quantity to change quantity.")

    conn.close()


# ========== UPDATE PRODUCT QUANTITY ==========
def update_quantity(sku, quantity_change):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM inventory WHERE sku=?", (sku,))
    row = cursor.fetchone()

    if row:
        new_quantity = row[0] + quantity_change
        cursor.execute("UPDATE inventory SET quantity=? WHERE sku=?", (new_quantity, sku))
        conn.commit()
        print(f"🔁 Quantity updated for {sku}. New quantity: {new_quantity}")
    else:
        print("❌ SKU not found.")

    conn.close()


# ========== VIEW ALL INVENTORY ==========
def view_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    print("\n📦 Current Inventory:")
    print("SKU\t\tProduct Name\t\tQuantity")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t\t{row[2]}")

    conn.close()


# ========== MAIN FUNCTION FOR TESTING ==========
if __name__ == "__main__":
    create_table()

    # Sample Test Data
    add_product('SKU123', 'Product A', 50)
    add_product('SKU456', 'Product B', 30)
    update_quantity('SKU123', -5)
    update_quantity('SKU999', 10)  # SKU doesn't exist
    view_inventory()
