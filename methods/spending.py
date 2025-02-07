import pandas as pd
from datetime import datetime
import os

class Spending:
    def __init__(self, paths):
        """
        Args:
            paths (dict): Dictionary of filepaths to westpac and anz spending data
        """
        self.paths = paths
        self.COLUMN_NAMES = ["Expense", "$", "Date"]
        self.anz_column_names = ["Date", "$", "Expense"]
        
        self.westpac_data = pd.read_csv(self.paths["Westpac"])
        self.anz_data = pd.read_csv(self.paths["ANZ"], header=None, names=self.anz_column_names)      
        
           
    def __clean_westpac_data(self):
        """Clean westpac spending data into consistent format with 3 columns - COLUMN_NAMES
        """
        self.westpac_data["Date"] = self.westpac_data["Date"].apply(
            lambda row_date: datetime.strptime(row_date, "%d/%m/%Y"))
        self.westpac_data = self.westpac_data[self.westpac_data["Debit Amount"] != 0] # remove unnecessary duplicate lines (like foreign fees)
        self.westpac_data["Debit Amount"] = self.westpac_data["Debit Amount"].fillna(-self.westpac_data["Credit Amount"])
             
        self.westpac_data = self.westpac_data[["Narrative", "Debit Amount", "Date"]]
        self.westpac_data.columns = self.COLUMN_NAMES
            
    def __clean_anz_data(self):
        """Clean anz spending data into consistent format with 3 columns - COLUMN_NAMES
        """
        self.anz_data["Date"] = self.anz_data["Date"].apply(
            lambda row_date: datetime.strptime(row_date, "%d/%m/%Y"))
        self.anz_data["$"] = -self.anz_data["$"]
        self.anz_data = self.anz_data[self.COLUMN_NAMES]
        
    def __special_clean(self, dirty_df):
        """Cleans merged data to match any special criteria

        Args:
            dirty_df (pd.DataFrame): DataFrame requiring final data cleaning / formatting

        Returns:
            pd.DataFrame: Fully cleaned DataFrame
        """
        #dirty_df.loc[dirty_df["Expense"].isin(["DEPOSIT-SALARY Comply HQ Pty Lt        Comply HQ Earnings", "INTEREST PAID" ]), "$"] *= -1
        dirty_df.loc[dirty_df["Expense"].str.contains("Siv - Stake Invest"), "$"] *= -1
        dirty_df.loc[dirty_df["Expense"].str.contains("PYMT Siv - Vang Invest"), "$"] *= -1
        
        # This removes account to account transfers including payment of credit card
        invalid_expenses = ["TFR", "PAYMENT - THANKYOU", "BPAY ANZ CARDS", "PYMT Siv - uBan Long-term Savings"]
        invalid_expenses = "|".join(invalid_expenses)
        
        dirty_df = dirty_df[~dirty_df["Expense"].str.contains(invalid_expenses, regex=True)]
        
        return dirty_df
    
    
    def get_spending_data(self):
        """Cleans all spending data

        Returns:
            pd.DataFrame: Fully cleaned DataFrame
        """
        self.__clean_westpac_data()
        self.__clean_anz_data()
        
        all_spending_data = pd.concat([self.westpac_data, self.anz_data])
        all_spending_data = all_spending_data.sort_values(by="Date")
        
        all_spending_data = self.__special_clean(all_spending_data)
        
        # for key, val in self.paths:
        #     os.remove(val)
        
        return all_spending_data
        
