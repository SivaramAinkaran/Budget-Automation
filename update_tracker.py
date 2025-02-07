import methods.login as login
import methods.expenses as expenses
import methods.spending as spending
import methods.update_database as update_database

import pandas as pd
import os
import tkinter as tk
import time

from tkinter import messagebox
from datetime import datetime

class NewSpending:
    
    def __init__(self):
        self.output_path = r"C:\Users\User\Downloads\expenses.csv"
        
        # data from expense tracker
        self.expenses = expenses.CurrentExpenses()
        self.expenses_data = self.expenses.expense_tracker()
        
        # data from card spending
        login.get_reports()
        time.sleep(3)
        self.report_file_paths = login.get_report_filepaths()
        
        self.spending = spending.Spending(self.report_file_paths)
        self.spending_data = self.spending.get_spending_data()
           
        self.Paths = {
            "Budget": "Finances/Budget/2024-2025/1 2024-2025.xlsx",
        }
         
    def __monthly_spending(self):
        current_month = self.expenses.current_month
        month_list = self.expenses.MONTHS
        
        current_month = month_list.index(current_month) + 1
               
        monthly_spending_data = self.spending_data[self.spending_data["Date"].dt.month == current_month]
        return monthly_spending_data        
        
    def get_new_expenses(self):        
        
        self.spending_data = self.__monthly_spending()   
        
        self.expenses_data["source"] = "Expenses"
        
        new_spending_data = pd.merge(self.spending_data, self.expenses_data, on=["Expense", "$", "Date"], how="outer")
        new_spending_data = new_spending_data[new_spending_data["source"].isna()]
        new_spending_data = new_spending_data.drop(columns=["source"])        
        new_spending_data.to_csv(self.output_path, index=False)
        os.startfile(self.output_path)
    
def refresh_database():
    if datetime.now().month <= 6:
        current_year = datetime.now().year-1
    else:
        current_year = datetime.now().year
        
    expense_tracker_path = r"C:\Users\User\Documents\[03] Shortcuts\Finances\Budget"
    current_year_folder = os.path.join(expense_tracker_path, f"{current_year}-{current_year + 1}")
    os.startfile(os.path.join(current_year_folder, "1 2024-2025.xlsx"))
    
    root = tk.Tk()
    root.withdraw()
    ok_clicked = messagebox.askokcancel(title="Update Database?", message="Click ok once you have updated, saved and closed your budget to update the Database")
    if ok_clicked:
        update_database.update_database(current_year_folder)
        os.startfile(r"C:\Users\User\Documents\[03] Shortcuts\Finances\Budget\Power BI\Expense Report.pbix")
    root.destroy()
    
    
    

output_new_spending = NewSpending()
output_new_spending.get_new_expenses()
refresh_database()







    
    



    
    





















