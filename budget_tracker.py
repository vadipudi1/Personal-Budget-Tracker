import pandas as pd
import matplotlib.pyplot as plt

class BudgetTracker:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])
    
    def add_entry(self, date, category, description, amount):
        new_entry = pd.DataFrame({'Date': [date], 'Category': [category], 'Description': [description], 'Amount': [amount]})
        self.data = pd.concat([self.data, new_entry], ignore_index=True)
    
    def view_entries(self):
        return self.data
    
    def delete_entry(self, index):
        self.data = self.data.drop(index, axis=0).reset_index(drop=True)
    
    def summarize_by_category(self):
        return self.data.groupby('Category')['Amount'].sum()
    
    def plot_expenses(self):
        summary = self.summarize_by_category()
        summary.plot(kind='bar')
        plt.title('Expenses by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.show()
    
    def search_entries(self, keyword):
        return self.data[self.data.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    
    def export_to_csv(self, filename):
        self.data.to_csv(filename, index=False)
    
    def import_from_csv(self, filename):
        self.data = pd.read_csv(filename)

