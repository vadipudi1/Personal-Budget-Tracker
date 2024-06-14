

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from budget_tracker import BudgetTracker

class BudgetApp:
    def __init__(self, root):
        self.tracker = BudgetTracker()
        
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.root.geometry("800x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create input fields
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        self.date_label = tk.Label(input_frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.category_label = tk.Label(input_frame, text="Category:")
        self.category_label.grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = ttk.Combobox(input_frame, values=[
            "Food", "Entertainment", "Utilities", "Transport", "Healthcare", 
            "Education", "Housing", "Insurance", "Savings", "Investments", "Other"
        ])
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)
        self.category_entry.set("Select Category")
        
        self.description_label = tk.Label(input_frame, text="Description:")
        self.description_label.grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(input_frame)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.amount_label = tk.Label(input_frame, text="Amount:")
        self.amount_label.grid(row=1, column=2, padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=3, padx=5, pady=5)
        
        self.add_button = tk.Button(input_frame, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=2, column=0, columnspan=4, pady=5)
        
        self.search_label = tk.Label(input_frame, text="Search:")
        self.search_label.grid(row=3, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(input_frame)
        self.search_entry.grid(row=3, column=1, padx=5, pady=5)
        self.search_button = tk.Button(input_frame, text="Search", command=self.search_entries)
        self.search_button.grid(row=3, column=2, padx=5, pady=5)
        
        self.export_button = tk.Button(input_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.import_button = tk.Button(input_frame, text="Import from CSV", command=self.import_from_csv)
        self.import_button.grid(row=4, column=2, columnspan=2, pady=5)
        
        # Create Treeview
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=('Date', 'Category', 'Description', 'Amount'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Amount', text='Amount')
        self.tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Create buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.view_button = tk.Button(button_frame, text="View Entries", command=self.view_entries)
        self.view_button.grid(row=0, column=0, padx=10)
        
        self.delete_button = tk.Button(button_frame, text="Delete Entry", command=self.delete_entry)
        self.delete_button.grid(row=0, column=1, padx=10)
        
        self.plot_button = tk.Button(button_frame, text="Plot Expenses", command=self.plot_expenses)
        self.plot_button.grid(row=0, column=2, padx=10)
    
    def add_entry(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        
        if not date or category == "Select Category" or not description or not amount:
            messagebox.showwarning("Input Error", "All fields are required")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number")
            return
        
        self.tracker.add_entry(date, category, description, amount)
        messagebox.showinfo("Success", "Entry added successfully")
        
        self.date_entry.delete(0, tk.END)
        self.category_entry.set("Select Category")
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.view_entries()
    
    def view_entries(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for index, row in self.tracker.view_entries().iterrows():
            self.tree.insert('', 'end', values=(row['Date'], row['Category'], row['Description'], row['Amount']))
    
    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No item selected")
            return
        
        for item in selected_item:
            item_values = self.tree.item(item, 'values')
            item_index = self.tracker.view_entries()[
                (self.tracker.view_entries()['Date'] == item_values[0]) &
                (self.tracker.view_entries()['Category'] == item_values[1]) &
                (self.tracker.view_entries()['Description'] == item_values[2]) &
                (self.tracker.view_entries()['Amount'] == item_values[3])
            ].index[0]
            self.tracker.delete_entry(item_index)
            self.tree.delete(item)
        
        messagebox.showinfo("Success", "Entry deleted successfully")
    
    def plot_expenses(self):
        self.tracker.plot_expenses()
    
    def search_entries(self):
        keyword = self.search_entry.get()
        filtered_data = self.tracker.search_entries(keyword)
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for index, row in filtered_data.iterrows():
            self.tree.insert('', 'end', values=(row['Date'], row['Category'], row['Description'], row['Amount']))
    
    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.tracker.export_to_csv(filename)
            messagebox.showinfo("Success", "Data exported successfully")
    
    def import_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.tracker.import_from_csv(filename)
            messagebox.showinfo("Success", "Data imported successfully")
            self.view_entries()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
