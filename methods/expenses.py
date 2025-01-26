import pandas as pd
import os
from tkinter import simpledialog
from datetime import datetime, date

class CurrentExpenses:
    """Get all Expenses for the given month currently in budget
    """
    
    def __init__(self):
        self.MONTHS = ["JANUARY", 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        self.SHORT_MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        self.EXPENSE_TYPES = ["Income", "Variable Expenses", "Fixed Expenses", "Investments"]
             
        self.current_month = self.MONTHS[datetime.now().month - 1]
        
        self.dialog_messages = {
            "message_get_month" : f"Current Month: {self.current_month} \nPress ok to continue or type in the desired month",
            "message_invalid_month" : f"Invalid Month!\nCurrent Month: {self.current_month} \nPress ok to continue or type in the desired month"
        }
        
        self.file_paths = {
            "expense_tracker": r"C:\Users\User\Documents\[03] Shortcuts\Finances\Budget"
        }
        
        if self.current_month in self.MONTHS[:5]:
            self.current_year = datetime.now().year-1
        else:
            self.current_year = datetime.now().year
                
    
    def __check_valid_month(self, user_month):
        """Gets user input for month they want expenses for. Checks if input is a valid value

        Args:
            user_month (str): Month value input by user

        Returns:
            str OR bool: user input month OR False if invalid month entered
        """
                
        input_month = False
                
        if len(user_month) == 0:
            input_month = self.current_month
        elif user_month.isdigit():
            user_month = int(user_month)
            if user_month in range(1, 13):
                input_month = self.MONTHS[user_month - 1]
            else:
                pass
        elif user_month.upper() in self.MONTHS:
            input_month = user_month
        elif user_month.upper() in self.SHORT_MONTHS:
            input_month = self.MONTHS[self.SHORT_MONTHS.index(user_month.upper())]
            
        return input_month
        
        
    def get_month(self):
        """Get month to update expenses for it

        Returns:
            str: str value for current_month
        """
        
        current_month = simpledialog.askstring("Month", self.dialog_messages["message_get_month"]) 
        
        while not self.__check_valid_month(self.current_month):
            self.current_month = simpledialog.askstring("Month", self.dialog_messages["message_invalid_month"]) 
        self.current_month = self.__check_valid_month(current_month) # default to current month when left blank
        
        return self.current_month
      
    
    def __clean_tracker(self, expense_data):
        
        """Collates expense tracker into 1 table of all expenses

        Parameters
        ----------
        expense_data (pd.DataFrame): Sheet of expenses for that month

        Returns
        -------
        all_expense_data (pd.DataFrame): DataFrame of all expense data for the month
            

        """
        default_column_names = ["Expense", "$", "Date", "Source"]
        
        tracker_columns = expense_data.columns.tolist()        
        expense_indexes = [tracker_columns.index(column_name) for column_name in self.EXPENSE_TYPES]
        
        all_expense_data = []        
        for expense_type_index in expense_indexes:
            expense_type_data = expense_data.iloc[:,expense_type_index:expense_type_index+4]
            expense_type_data.columns = default_column_names
            expense_type_data.drop(columns="Source", inplace=True)
            expense_type_data.dropna(how="all", inplace=True)
            all_expense_data.append(expense_type_data)
        
        all_expense_data = pd.concat(all_expense_data)
        
        return all_expense_data

    def expense_tracker(self):
        """_summary_

        Args:
            budget_pth (_type_): _description_
            curr_yr (_type_): _description_
            curr_mth_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.get_month()
        current_year_folder = os.path.join(self.file_paths["expense_tracker"], f"{self.current_year}-{self.current_year + 1}")
        
        for file in os.listdir(current_year_folder):
            if self.current_month in file:
                expense_tracker_path = os.path.join(current_year_folder, file)
                
        with pd.ExcelFile(expense_tracker_path) as expense_data:
            expense_data = expense_data.parse(sheet_name=expense_data.sheet_names[0])
            expense_data = self.__clean_tracker(expense_data)
            
        return expense_data
        
        


if __name__ == "__main__":
    print("hello")
        
        
        
