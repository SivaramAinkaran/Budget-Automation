import pandas as pd 
import numpy as np
import os
from tkinter import filedialog, messagebox
from datetime import datetime

# TODO include all future budgets as well to prevent deprecation
# TODO remove reliance on explicit filepaths

def update_database(folder_path=r"C:\Users\User\Documents\[03] Shortcuts\Finances\Budget\2024-2025"):
    """Extracts all existing budget data for given financial years and collates into csv database for Power BI

    Args:
        folder_path (regexp, optional): Path to main budget folder. Defaults to r"C:\Users\User\Documents\[03] Shortcuts\Finances\Budget\2024-2025".
    """
    # TODO remove reliance on list by just searching folder
    FILES = ['1. JULY.xlsx', '2. AUGUST.xlsx', '3. SEPTEMBER.xlsx', '4. OCTOBER.xlsx', '5. NOVEMBER.xlsx', 
             '6. DECEMBER.xlsx', '7. JANUARY.xlsx', '8. FEBRUARY.xlsx', '9. MARCH.xlsx', '10. APRIL.xlsx', 
             '11. MAY.xlsx', '12. JUNE.xlsx']
    
    all_formatted_data = []
    for file in FILES:
        file_path = os.path.join(folder_path, file)
        budget_data = pd.read_excel(file_path, sheet_name='Tracker')
        formatted_data = format_data(budget_data)
        if len(all_formatted_data) == 0:
            all_formatted_data = formatted_data
        else:
            all_formatted_data = pd.concat([all_formatted_data, formatted_data])
        
    all_formatted_data.to_csv(r"C:\Users\User\Documents\[03] Shortcuts\Finances\Budget\Power BI\All Expenses.csv", index=False)
    
    return
        
def format_data(data):
    """Formats budget data into 1 usable database

    Args:
        data (pd.DataFrame): data captured in that month's budget spreadsheet

    Returns:
        _type_: _description_
    """
    income = data.iloc[:, 0:4]
    income.columns = ["Description", "$", "Date", "Source"]
    income["Type"] = "Income"
    income.dropna(subset=["Description", "$", "Source"], inplace=True)
    
    variable_expenses = data.iloc[:, 5:9]
    variable_expenses.columns = ["Description", "$", "Date", "Source"]
    variable_expenses["Type"] = "Variable Expenses"
    variable_expenses.dropna(subset=["Description", "$", "Source"], inplace=True)
    
    fixed_expenses = data.iloc[:, 10:14]
    fixed_expenses.columns = ["Description", "$", "Date", "Source"]
    fixed_expenses["Type"] = "Fixed Expenses"
    fixed_expenses.dropna(subset=["Description", "$", "Source"], inplace=True)
    
    investments = data.iloc[:, 15:19]
    investments.columns = ["Description", "$", "Date", "Source"]
    investments["Type"] = "Investments"
    investments.dropna(subset=["Description", "$", "Source"], inplace=True)
    
    all_data = pd.concat([income, variable_expenses, fixed_expenses, investments])
    all_data.dropna(subset=["Description", "$", "Source"], inplace=True)
    
    return all_data


if __name__ == "__main__":
    update_database()