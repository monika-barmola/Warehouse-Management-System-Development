import sqlite3
import pandas as pd

def generate_inventory_report():
    # Connect to inventory database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Fetch inventory data
    cursor.execute("SELECT SKU, Name, Quantity FROM inventory")
    rows = cursor.fetchall()

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=["SKU", "Product Name", "Quantity"])

    # Export to Excel
    output_file = "inventory_report.xlsx"
    df.to_excel(output_file, index=False)

    print(f"✅ Report generated successfully: {output_file}")

    conn.close()

if __name__ == "__main__":
    generate_inventory_report()
