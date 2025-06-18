import tkinter as tk
from tkinter import ttk
import sqlite3

class InventoryViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WMS Inventory Viewer")
        self.root.geometry("600x400")

        # Create Treeview (table)
        self.tree = ttk.Treeview(root, columns=("SKU", "Name", "Quantity"), show="headings")
        self.tree.heading("SKU", text="SKU")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Quantity", text="Quantity")

        self.tree.column("SKU", width=150)
        self.tree.column("Name", width=300)
        self.tree.column("Quantity", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load data
        self.load_inventory()

    def load_inventory(self):
        try:
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()

            # Fetch data
            cursor.execute("SELECT SKU, Name, Quantity FROM inventory")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)

            conn.close()

        except Exception as e:
            print("❌ Error loading inventory:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryViewerApp(root)
    root.mainloop()
