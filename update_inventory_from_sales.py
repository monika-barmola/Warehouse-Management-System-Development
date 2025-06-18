import sqlite3
import openpyxl
from tkinter import messagebox

# Load sales data from Excel
def load_sales_data(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    sales_data = []

    # Assuming first row is headers
    for row in sheet.iter_rows(min_row=2, values_only=True):
        sku = row[1]  # Column B (index 1)
        quantity = row[7]  # Column H (index 7)
        if sku and isinstance(quantity, (int, float)):
            sales_data.append((sku.strip(), abs(int(quantity))))  # Convert to positive

    return sales_data

# Update inventory based on sales
def update_inventory(sales_data):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    updated_count = 0
    not_found_count = 0

    for sku, sold_quantity in sales_data:
        cursor.execute("SELECT Quantity FROM inventory WHERE SKU = ?", (sku,))
        result = cursor.fetchone()

        if result:
            current_quantity = result[0]
            new_quantity = max(0, current_quantity - sold_quantity)
            cursor.execute("UPDATE inventory SET Quantity = ? WHERE SKU = ?", (new_quantity, sku))
            updated_count += 1
        else:
            not_found_count += 1

    conn.commit()
    conn.close()

    return updated_count, not_found_count

# Main function
if __name__ == "__main__":
    try:
        file_path = "sales_mapped.xlsx"
        sales_data = load_sales_data(file_path)
        updated, not_found = update_inventory(sales_data)
        messagebox.showinfo("Update Complete", f"Inventory updated.\nSKUs updated: {updated}\nSKUs not found: {not_found}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
