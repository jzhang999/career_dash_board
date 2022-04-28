
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:08:56 2022

@author: watercross
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter
import numpy as np

options = webdriver.ChromeOptions()

s = Service(r'C:\Users\watercross\Downloads\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(service=s)

def scraping_company(company_name):
    url = 'https://www.glassdoor.com/Interview/pittsburgh-microsoft-interview-questions-SRCH_IL.0,10_IM684_KE11,20_IP2.htm'
    driver.get(url)
    
    workbook = xlsxwriter.Workbook('glassdoor.xlsx')
    worksheet = workbook.add_worksheet()
    questions = []
    
    page_question = driver.find_element(By.XPATH, '//*[@id="BaseLayout"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/h3').text
    time.sleep(2)
    page_date = driver.find_element(By.XPATH, '//*[@id="BaseLayout"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/span[2]').text
    time.sleep(2)
    question =[]
    question.append(page_question)
    question.append(page_date)
    questions.append(question)
    
    driver.find_element(By.XPATH, "//*[@id='BaseLayout']/div/div[1]/div[1]/div[2]/div[3]/div[2]/div/div[1]/button[2]").click()
    
    
    driver.find_element(By.XPATH, '//*[@id="HardsellOverlay"]/div/div/div/div/div[2]/div/a').click()
    
    name = driver.find_element(By.ID, "hardsellUserEmail" )
    
    pwd = driver.find_element(By.ID, "hardsellUserPassword")
    name.send_keys("ilmhsusan@gmail.com")
    pwd.send_keys("Mau67%kkk")
    
    driver.find_element(By.XPATH,'//*[@id="HardsellOverlay"]/div/div/div/div/div[1]/div/form/div[3]/button').click()
    delay = 100
   
    while len(questions) < 50:
        try:
            page_question = driver.find_element(By.XPATH, '//*[@id="BaseLayout"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/h3').text
            
        except:
            time.sleep(2)
            driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/p/a').click()
            time.sleep(2)
            page_question = driver.find_element(By.XPATH, '//*[@id="BaseLayout"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/h3').text
        time.sleep(2)
        try:
            page_date = driver.find_element(By.XPATH, '//*[@id="BaseLayout"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/span[2]').text
        except:
            pass
        time.sleep(2)
        question =[]
        question.append(page_question)
        question.append(page_date)
        questions.append(question)
        try: 
            button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='BaseLayout']/div/div[1]/div[1]/div[2]/div[3]/div[2]/div/div[1]/button[2]")))
            time.sleep(2)
            ActionChains(driver).move_to_element(button).click(button).perform()
        except ElementClickInterceptedException:
            pass
    
    row = 0
    col = 0
    # # Iterate over the data and write it out row by row.
    a1 = np.array(questions,dtype=object)
    
    df =pd.DataFrame(a1,columns = ['question', 'date'])
    df.to_csv(company_name + '.csv')
scraping_company('microsoft')
print("microsoft is finished.")

   
    
    
