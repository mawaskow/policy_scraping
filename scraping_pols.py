from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

dir = "C:\\Users\\Ales\\Documents\\PhD"

# initialize driver
web = "https://www.gov.ie/en/policies/"
driver = webdriver.Chrome()
time_start=time.time()
driver.get(web)
driver.maximize_window()

# get site count of policy categories, for sanity check and for funsies
pol_domain_ct = driver.find_element(by='xpath', value='//strong').text
pol_domain_ct = int(pol_domain_ct.split(" ")[0])

# list of policy domain elements, create dictionary of key- domain name, and value- hyperlink
dom_lst = driver.find_elements(by='xpath', value='//a[contains(@title, "Policy")]')
dom_links = {}
for i in dom_lst:
    dom_links[i.text] = i.get_attribute('href')

# try a single site with many pages
driver.get(dom_links['Tourism']+"latest")

result_title = []
result_href = []
result_date = []
result_dept = []
result_type = []

# get results div
results_div = driver.find_element(by='xpath', value='//div[contains(@class, "reboot-content")]//ul')
result_name = results_div.find_elements(by='xpath', value='.//a')

for i in result_name:
    result_title.append(i.text)
    result_href.append(i.get_attribute('href'))
    try:
        result_p = i.find_element(by='xpath', value='..//p').text.split(";")
        result_date.append(result_p[0])
        result_dept.append(result_p[1])
        result_type.append(result_p[2])
    except:
        result_date.append('err')
        result_dept.append('err')
        result_type.append('err')

df = pd.DataFrame(data={"Title":result_title, "Date":result_date, "Type":result_type, "Department":result_dept, "href":result_href})
df.to_csv(f"{dir}\\tourism.csv", index=False)

# for each policy domain, open the link [outer loop] 
'''
for i in dom_links.keys():
    driver.get(dom_links[i]+"latest")
'''
driver.quit()
print(f"Run in {time.time()-time_start}s")