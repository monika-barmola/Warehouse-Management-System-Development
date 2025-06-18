import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import sqlite3
import pandas as pd

DB_NAME = "inventory.db"

class WMSApp:
    def __init__(self, root):
        self.root = root
        root.title("Warehouse Management System")
        root.geometry("400x400")

        tk.Button(root, text="📦 View Inventory", width=30, command=self.view_inventory).pack(pady=10)
        tk.Button(root, text="➕ Add Product", width=30, command=self.add_product).pack(pady=10)
        tk.Button(root, text="🔁 Update Quantity", width=30, command=self.update_quantity).pack(pady=10)
        tk.Button(root, text="📂 Upload Sales Excel", width=30, command=self.update_inventory_from_sales).pack(pady=10)
        tk.Button(root, text="📊 Generate Report", width=30, command=self.generate_report).pack(pady=10)

    def connect_db(self):
        return sqlite3.connect(DB_NAME)

    def view_inventory(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT SKU, Name, Quantity FROM inventory")
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                messagebox.showinfo("Inventory", "No inventory records found.")
                return

            view_win = tk.Toplevel(self.root)
            view_win.title("Inventory List")

            for i, row in enumerate(rows):
                text = f"{row[0]} - {row[1]} - Qty: {row[2]}"
                tk.Label(view_win, text=text).pack(anchor="w")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_product(self):
        sku = simpledialog.askstring("SKU", "Enter SKU:")
        name = simpledialog.askstring("Product Name", "Enter product name:")
        qty = simpledialog.askinteger("Quantity", "Enter quantity:")

        if not (sku and name and qty is not None):
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO inventory (SKU, Name, Quantity) VALUES (?, ?, ?)", (sku, name, qty))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"✅ Product '{name}' added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_quantity(self):
        sku = simpledialog.askstring("SKU", "Enter SKU to update:")
        qty = simpledialog.askinteger("Quantity", "Enter new quantity:")

        if not (sku and qty is not None):
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET Quantity=? WHERE SKU=?", (qty, sku))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "SKU not found.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "✅ Quantity updated.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_inventory_from_sales(self):
        sales_file = filedialog.askopenfilename(title="Select Sales Excel", filetypes=[("Excel files", "*.xlsx")])
        if not sales_file:
            return
        try:
            sales_df = pd.read_excel(sales_file)

            if "SKU" not in sales_df.columns or "Quantity" not in sales_df.columns:
                messagebox.showerror("Error", "Excel must have 'SKU' and 'Quantity' columns.")
                return

            conn = self.connect_db()
            cursor = conn.cursor()

            for _, row in sales_df.iterrows():
                sku = row["SKU"]
                qty = int(abs(row["Quantity"]))  # make quantity positive
                cursor.execute("UPDATE inventory SET Quantity = Quantity - ? WHERE SKU = ?", (qty, sku))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "✅ Inventory updated from sales.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_report(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT SKU, Name, Quantity FROM inventory")
            rows = cursor.fetchall()
            conn.close()

            df = pd.DataFrame(rows, columns=["SKU", "Product Name", "Quantity"])
            df.to_excel("inventory_report.xlsx", index=False)
            messagebox.showinfo("Success", "✅ Report saved as 'inventory_report.xlsx'")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WMSApp(root)
    root.mainloop()
