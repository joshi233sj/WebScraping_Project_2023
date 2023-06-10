from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import re
import time
import pandas as pd

#setting chrome driver path
# Init:
gecko_path = '/usr/local/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'https://www.careers360.com/colleges/india-colleges-fctp?page=1'

#calling the website url
driver.get(url)

#maximizing the browser window
#driver.maximize_window()

# setting boolean parameter for page limit
page_limit = True

if page_limit == True:
    max_pages = 2
else: max_pages = 100



# declaring lists to store scraped data
schoolName_list = []
course_list = []
sectors_list = []
links_list=[]



# iterating over first 100 pages to scrap required data
time.sleep(12)
driver.find_element(By.CLASS_NAME, value='closebtnSignIn').click()

for i in range(1,max_pages+1):
    
    time.sleep(1)
    names = driver.find_elements(By.XPATH,'//div[@class="tupple_right_block d-none d-md-block"]/h3/a')
    for name in range(len(names)):
        schoolName_list.append(names[name].text) 

    time.sleep(1)
    course = driver.find_elements(By.XPATH,'//div[@class="left_side_tupple"]/a[contains(@class,"general_text")]')
    for cs in range(len(course)):
        course_list.append(course[cs].text)

    time.sleep(1)
    sectros = driver.find_elements(By.XPATH,'//div[@class="content_block d-none d-md-block d-md-flex flex-row justify-content-between"]/div/span[2]')
    for sectro in range(len(sectros)):
        sectors_list.append(sectros[sectro].text)

    time.sleep(1)
    Links = driver.find_elements(By.XPATH,'//div[@class="tupple_right_block d-none d-md-block"]/h3/a')
    for link in range(len(Links)):
        links_list.append(Links[link].get_attribute('href'))

     
    # using time.sleep for a slight delay in code to interact and find all the elements
    time.sleep(1)
    driver.get('https://www.careers360.com/colleges/india-colleges-fctp?page='+str(i))


    
    
   
# creating a dictionary to store the scraped data in previous step
data_dictionary = {'Name': schoolName_list, 'Course': course_list, 'Sector': sectors_list, 'Links' : links_list }

# storing the scraped data in csv file
#dataframe = pd.DataFrame(data_dictionary)
#dataframe.to_csv('data.csv', mode='a', index=False, header=False, encoding="cp1252")
df = pd.DataFrame.from_dict(data_dictionary, orient='index')
df = df.transpose()
df = df.sort_values(by=['Name'], ascending=True)
df.to_csv('data_selenium.csv', index = False)




# closing the driver instance and browser window
driver.quit()

