import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class SKUMappingApp:
    def __init__(self, master):
        self.master = master
        master.title("WMS - SKU to MSKU Mapper")

        # Upload buttons
        self.label = tk.Label(master, text="Upload Sales File:")
        self.label.pack()

        self.upload_button = tk.Button(master, text="Upload Excel", command=self.load_sales_data)
        self.upload_button.pack()

        self.map_button = tk.Button(master, text="Map SKUs", command=self.map_skus)
        self.map_button.pack()

        self.export_button = tk.Button(master, text="Export Mapped File", command=self.export_file)
        self.export_button.pack()

        self.status = tk.Label(master, text="")
        self.status.pack()

        self.sales_df = None
        self.mapping_df = None

        # Load mapping file automatically
        try:
            self.mapping_df = pd.read_excel("sku_mapping.xlsx")
        except:
            self.status.config(text="⚠️ Missing sku_mapping.xlsx file")

    def load_sales_data(self):
        file_path = filedialog.askopenfilename(title="Select sales Excel file", filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                self.sales_df = pd.read_excel(file_path)
                self.status.config(text="✅ Sales file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def map_skus(self):
        if self.sales_df is None or self.mapping_df is None:
            messagebox.showerror("Error", "Sales data or mapping file not loaded")
            return
        try:
            self.sales_df = pd.merge(self.sales_df, self.mapping_df, how="left", on="SKU")
            self.status.config(text="✅ SKUs mapped to MSKUs")
        except Exception as e:
            messagebox.showerror("Mapping Error", str(e))

    def export_file(self):
        if self.sales_df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", title="Save Mapped File")
            if file_path:
                try:
                    self.sales_df.to_excel(file_path, index=False)
                    self.status.config(text=f"✅ Exported to {file_path}")
                except Exception as e:
                    messagebox.showerror("Export Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SKUMappingApp(root)
    root.mainloop()
