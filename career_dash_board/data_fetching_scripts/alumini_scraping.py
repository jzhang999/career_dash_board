# -*- coding: utf-8 -*-
"""
Python script to get the alumni numbers for universities

@author: Jing Zhang
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import time
import pandas as pd


def wait(driver, timeout=1):
    prev_src = driver.page_source
    elapsed = 0
    unit_time = timeout / 10
    while prev_src == driver.page_source and elapsed <= timeout:
        time.sleep(unit_time)
        timeout -= unit_time
        elapsed += unit_time


def login(driver):
    url = 'https://www.linkedin.com/'
    driver.get(url)
    username = driver.find_element_by_xpath('//input[@id="session_key"]')
    password = driver.find_element_by_xpath('//input[@id="session_password"]')
    signin_button = driver.find_element_by_xpath('//button[@class="sign-in-form__submit-button"]')
    username.send_keys('your username')  # TODO: fill in please
    password.send_keys('your password')  # TODO: fill in please
    signin_button.click()
    wait(driver, 1)
    print('successfully logged in!')


def get_all_schools_info(driver, target_company='meta'):
    url = 'https://www.linkedin.com/company/{}/people/'.format(target_company)
    driver.get(url)
    time.sleep(2)
    showmore_button = driver.find_element_by_xpath(
        '//button[@class="org-people__show-more-button t-16 t-16--open t-black--light t-bold"]')
    showmore_button.click()
    wait(driver, 1)
    schools = driver.find_elements_by_xpath(
        '//div[@class="org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"]')
    all_schools_info = {}
    for school in schools:
        raw_info = school.text
        if raw_info:
            info_list = raw_info.split()
            num_alumni = int(info_list[0].replace(',', ''))
            school_name = ' '.join(info_list[1:])
            all_schools_info[school_name] = num_alumni

    return all_schools_info


def get_target_school_info(all_schools_info, target_company, target_school='Carnegie Mellon University'):
    lowest_rank = sorted(all_schools_info.items(), key=lambda x: x[1])[0]
    if target_school in all_schools_info:
        return all_schools_info[target_school]
    else:
        print(f"using {lowest_rank[0]}\'s alumni count as a replacement for {target_company.capitalize()}")
        return lowest_rank[1]


def get_alumni_table(companies, target_school):
    print(f'Getting Alumni for {target_school}')
    alumni_table = {company.capitalize(): -1 for company in companies}
    for company in companies:
        all_schools_info = get_all_schools_info(driver, target_company=company)
        alumni_table[company.capitalize()] = get_target_school_info(all_schools_info, target_company=company,
                                                                    target_school=target_school)
    return alumni_table


def get_alumni_by_company(target_company,
                          school_url='https://www.linkedin.com/school/carnegie-mellon-university/people/'):
    driver.get(school_url)
    time.sleep(2)
    search_field = driver.find_element_by_xpath('//input[@id="people-search-keywords"]')
    search_field.send_keys(target_company)
    search_field.send_keys(u'\ue007')  # enter key
    wait(driver, 2)
    companies = driver.find_elements_by_xpath(
        '//div[@class="org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"]')
    for company in companies:
        raw_info = company.text
        if raw_info:
            info_list = raw_info.split()
            num_alumni = int(info_list[0].replace(',', ''))
            company_name = ' '.join(info_list[1:])
            if (company_name.lower() == target_company.lower()):
                print(f'{target_company} has {num_alumni} alumni')
                return num_alumni


if __name__ == '__main__':
    options = Options()
    options.headless = True

    # create Chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(20)
    login(driver)


    company_table = []
    companies = ['meta', 'amazon', 'apple', 'google', 'microsoft', 'salesforce', 'adobe']

    # get all company info we needed
    for company in companies:
        all_schools_info = get_all_schools_info(driver, company)
        for school, alumni in all_schools_info.items():
            company_table.append((company.capitalize(), school, alumni))

    company_df = pd.DataFrame(company_table)
    company_df.columns = ['company', 'university/region', 'alumni_count']
    company_df.to_csv('linkedin_companies.csv', index=False)

    cmu_alumni_table = {}
    companies = ['meta', 'amazon', 'apple', 'google', 'microsoft', 'salesforce', 'adobe']

    for company in companies:
        cmu_alumni_table[company.capitalize()] = get_alumni_by_company(company,
                                                                       school_url="https://www.linkedin.com/school/university-of-illinois-urbana-champaign/people/")
    cmu_alumni_table

    cmu_alumni_df = pd.DataFrame(cmu_alumni_table.items())
    cmu_alumni_df.columns = ['company', 'alumni_count']
    cmu_alumni_df.to_csv('alumni.csv', index=False)