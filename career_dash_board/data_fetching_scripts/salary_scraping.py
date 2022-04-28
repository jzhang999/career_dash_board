# coding=utf-8
import time
import csv

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

company_list = ["https://www.glassdoor.com/Salary/Google-Engineering-Salaries-EI_IE9079.0,6_DEPT1007.htm",
                "https://www.glassdoor.com/Salary/Amazon-Engineering-Salaries-EI_IE6036.0,6_DEPT1007.htm",
                "https://www.glassdoor.com/Salary/Meta-Engineering-Salaries-EI_IE40772.0,4_DEPT1007.htm",
                "https://www.glassdoor.com/Salary/Microsoft-Engineering-Salaries-EI_IE1651.0,9_DEPT1007.htm",
                "https://www.glassdoor.com/Salary/Apple-Engineering-Salaries-EI_IE1138.0,5_DEPT1007.htm",
                "https://www.glassdoor.com/Salary/Salesforce-Engineering-Salaries-EI_IE11159.0,10_DEPT1007.htm",
                "https://www.glassdoor.com/Salary/Adobe-Engineering-Salaries-EI_IE1090.0,5_DEPT1007.htm"
                ]

company_names = ['Google', 'Amazon', 'Meta', 'Microsoft', 'Apple', 'Salesforce', 'Adobe']

class Spider(object):
    # create Chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.implicitly_wait(20)

    def run(self):
        page_num = 0  # current page we are getting the data

        # login
        self.driver.get("https://www.glassdoor.com/member/home/index.htm")
        self.driver.find_element_by_id('inlineUserEmail').send_keys("your user name") # TODO: fill in please
        self.driver.find_element_by_id('inlineUserPassword').send_keys("your password") # TODO: fill in please
        self.driver.find_element_by_xpath('//*[@id="InlineLoginModule"]/div/div[1]/div/form/div[3]/button').click()

        # load the page
        time.sleep(10)

        # list of dicts to store the info
        comp_info = []
        # move to next page
        while page_num < len(company_list):
            # use get to open the page
            self.driver.get(company_list[page_num])

            # load the page
            time.sleep(20)

            salaries_x_path = '//*[@id="SalariesRef"]'
            parent_div = self.driver.find_element_by_xpath(salaries_x_path)
            count_of_divs = len(parent_div.find_elements_by_xpath("./div"))  # num salary infos in the salaries div

            for i in range(1, count_of_divs + 1):
                job_title = self.driver.find_element_by_xpath(
                    salaries_x_path + '/div[' + str(i) + ']/div/div[1]/div/a/strong').text

                salary = self.driver.find_element_by_xpath(
                    salaries_x_path + '/div[' + str(i) + ']/div/div[2]/div[1]/span[1]/span/strong/strong').text

                print(job_title, ': ', salary)

                comp_info.append({'company_info': company_names[page_num] + " " + job_title + " " + salary})
            page_num += 1

        print(comp_info)

        # write csv
        with open('company_salary_info.csv', mode='w') as csv_file:
            fieldnames = ['company_info']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for info in comp_info:
                writer.writerow(info)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
