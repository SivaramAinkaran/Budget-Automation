import time
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Browser:
    browser, service = None, None
    
    def __init__(self):        
        self.service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=self.service)
        
    def open_page(self, url: str):
        self.browser.get(url)
    
    def close_browser(self):
        self.browser.close()
        
        
    def add_input(self, by: By, value: str, text: str):
        wait = WebDriverWait(self.browser, 20)
        field = wait.until(EC.visibility_of_element_located((by, value)))
        field.send_keys(text)

    def click_button(self, by: By, value: str):
        wait = WebDriverWait(self.browser, 20)
        wait.until(EC.visibility_of_element_located((by, value)))
        wait.until(EC.element_to_be_clickable((by, value)))
        button = self.browser.find_element(by=by, value=value)
        button.click()
        
        
    def download_report_westpac(self):
        self.open_page('https://banking.westpac.com.au/secure/banking/reportsandexports/exportparameters/2/')
        self.click_button(by=By.XPATH, value='//*[@id="form-displayreportdata"]/div[1]/fieldset[1]/div/div[3]/a')
        self.click_button(by=By.XPATH, value='//*[@id="form-displayreportdata"]/div[1]/fieldset[1]/div/div[3]/div/ol/li[4]/a')
        self.click_button(by=By.XPATH, value='//*[@id="form-displayreportdata"]/div[2]/button')
        time.sleep(2)
        
    def download_report_anz(self):
        self.click_button(by=By.XPATH, value='//*[@id="list-item-home-screen-list-display-0"]')
        time.sleep(1)
        self.click_button(by=By.XPATH, value='//*[@id="Transactionstab"]/div')
        self.click_button(by=By.XPATH, value='//*[@id="search-download"]/button[2]')
        self.click_button(by=By.XPATH, value='//*[@id="drop-down-search-transaction-account1-dropdown-field"]')
        self.click_button(by=By.XPATH, value='//*[@id="row"]/div[1]/div/div/div[1]/ul/li')
        self.click_button(by=By.XPATH, value='//*[@id="drop-down-search-duration1-dropdown-field"]')
        self.click_button(by=By.XPATH, value='//*[@id="Durationpanel"]/div[2]/div/div/div[1]/ul/li[6]')
        self.click_button(by=By.XPATH, value='//*[@id="footer-primary-button"]') 
        time.sleep(2)
        
    def login_westpac(self, username: str, password: str):
        self.add_input(by=By.XPATH, value='//*[@id="fakeusername"]', text=username)
        self.add_input(by=By.XPATH, value='//*[@id="password"]', text=password)
        self.click_button(by=By.XPATH, value='//*[@id="signin"]')
        self.download_report_westpac()
        
    def login_anz(self, username: str, password: str):
        self.add_input(by=By.XPATH, value='//*[@id="customerRegistrationNumber"]', text=username)
        self.add_input(by=By.XPATH, value='//*[@id="password"]', text=password)
        self.click_button(by=By.XPATH, value='//*[@id="root"]/div/main/div/div/div[1]/div/div/form/div[2]/div/button')
        self.download_report_anz()

def get_report_filepaths(directory_path=r"C:\Users\User\Downloads"):
    BANKS = ["Westpac", "ANZ"]
    
    file_names = os.listdir(directory_path)
    
    file_paths = [os.path.join(directory_path, name) for name in file_names]
    sorted_file_paths = sorted(file_paths, key=os.path.getctime)
    report_paths = sorted_file_paths[-2:]    
    report_paths_dict = dict(zip(BANKS, report_paths))
    
    return report_paths_dict

def get_reports():        
    browser = Browser()
    browser.open_page('https://banking.westpac.com.au/wbc/banking/handler?TAM_OP=login&segment=personal&logout=false')
    browser.login_westpac("username", "password")
    browser.open_page("https://login.anz.com/internetbanking")
    browser.login_anz("username", "password")
    
    return

