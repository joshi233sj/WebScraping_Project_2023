from bs4 import BeautifulSoup
import requests
from lxml import etree
import time
import pandas as pd


# setting boolean parameter for page limit
page_limit = True

if page_limit == True:
    max_pages = 10
else: max_pages = 100


# declaring lists to store scraped data
name_list = []
rank_list = []
sector_list = []
user_rating_list=[]



# iterating over first 100 pages to scrap required data
for i in range(1, max_pages+1):
    print('\n',i)
    url = 'https://www.careers360.com/colleges/india-colleges-fctp?page='+str(i)
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    
    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    dom = etree.HTML(str(soup))
    
    names = dom.xpath('//div[@class="tupple_right_block d-none d-md-block"]/h3/a')
    for name in range(len(names)):
        name_list.append(names[name].text) 
    
    course   = dom.xpath('//div[@class="left_side_tupple"]/a[contains(@class,"general_text")]')
    for c in range(len(course)):
        rank_list.append(course[c].text)   
        
    sectors =dom.xpath('//div[@class="content_block d-none d-md-block d-md-flex flex-row justify-content-between"]/div/span[2]')
    for sector in range(len(sectors)):
        sector_list.append(sectors[sector].text)
        
    links=dom.xpath('//div[@class="tupple_right_block d-none d-md-block"]/h3/a/@href')
    for link in range(len(links)):
        user_rating_list.append(links[link])
        
   
   
# creating a dictionary to store the scraped data in previous step
data_dictionary = {'Name': name_list, 'Rank': rank_list, 'Sector': sector_list, 'User Rating' : user_rating_list }


# storing the scraped data in csv file
#dataframe = pd.DataFrame(data_dictionary)
#dataframe.to_csv('data.csv', mode='a', index=False, header=False, encoding="cp1252")
df = pd.DataFrame.from_dict(data_dictionary, orient='index')
df = df.transpose()
df = df.sort_values(by=['Name'], ascending=True)
df.to_csv('data_bsoup.csv',index = False)

