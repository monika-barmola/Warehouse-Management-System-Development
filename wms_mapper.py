import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class WMSMapperApp:
    def __init__(self, root):
        self.sales_file = None
        self.mapping_file = None

        root.title("WMS Mapper")
        root.geometry("350x180")

        tk.Button(root, text="📂 Browse Sales File", command=self.browse_sales).pack(pady=5)
        tk.Button(root, text="📂 Browse Mapping File", command=self.browse_mapping).pack(pady=5)
        tk.Button(root, text="🔄 Map and Export", command=self.map_and_export).pack(pady=10)

    def browse_sales(self):
        self.sales_file = filedialog.askopenfilename(
            title="Select Sales Excel File", filetypes=[("Excel files", "*.xlsx")])
        if self.sales_file:
            print("✅ Selected Sales File:", self.sales_file)

    def browse_mapping(self):
        self.mapping_file = filedialog.askopenfilename(
            title="Select Mapping Excel File", filetypes=[("Excel files", "*.xlsx")])
        if self.mapping_file:
            print("✅ Selected Mapping File:", self.mapping_file)

    def map_and_export(self):
        if not self.sales_file or not self.mapping_file:
            messagebox.showerror("❌ Error", "Please select both sales and mapping files.")
            return

        try:
            sales_df = pd.read_excel(self.sales_file)
            mapping_df = pd.read_excel(self.mapping_file)

            print("Sales Columns:", sales_df.columns.tolist())
            print("Mapping Columns:", mapping_df.columns.tolist())

            # Ensure 'SKU' exists in both
            sales_sku_col = self.find_column(sales_df.columns, "SKU")
            mapping_sku_col = self.find_column(mapping_df.columns, "SKU")

            if not sales_sku_col or not mapping_sku_col:
                messagebox.showerror("❌ Error", "'SKU' column not found in one or both files.")
                return

            # Merge on SKU
            merged_df = pd.merge(sales_df, mapping_df, left_on=sales_sku_col, right_on=mapping_sku_col, how="left")

            output_file = "sales_mapped.xlsx"
            merged_df.to_excel(output_file, index=False)
            messagebox.showinfo("✅ Success", f"Mapped data exported to: {output_file}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"An error occurred:\n{e}")

    def find_column(self, columns, target):
        """Return the actual column name if 'target' (case-insensitive, stripped) matches."""
        for col in columns:
            if col.strip().lower() == target.strip().lower():
                return col
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = WMSMapperApp(root)
    root.mainloop()

