'''
Created on 
Course work: 
@author:
Source:
    
'''

# Import necessary modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.options import Options

load_dotenv()

DRIVER_PATH = os.environ.get('DRIVER_PATH')

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=DRIVER_PATH)

def startpy():

    driver.get("https://google.com")
    print(driver.title)


if __name__ == '__main__':
    startpy()