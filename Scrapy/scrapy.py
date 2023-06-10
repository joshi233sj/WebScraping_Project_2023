import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
import pandas as pandasForSortingCSV
page_limit = False

if page_limit == True:
    pages = 3
else:
    pages = 100

#Setting up CSV file
with open('data_scrapy.csv','w') as s: 
    s.write("Name,Course,Sector,Links\n")


class careerSpider(scrapy.Spider):

    name = 'careersspidey'
    allowed_domains = ['https://www.careers360.com']

    start_urls = ['https://www.careers360.com/colleges/india-colleges-fctp?page=']
    for i in range(2,pages+1):
        start_urls.append('https://www.careers360.com/colleges/india-colleges-fctp?page=' + str(i))  
    

    def parse(self, response):
        schoolName_list = response.xpath('//div[@class="tupple_right_block d-none d-md-block"]/h3/a/text()').extract()
        course_list = response.xpath('//div[@class="left_side_tupple"]/a[contains(@class,"general_text")]/text()').extract()
        sectors_list = response.xpath('//div[@class="content_block d-none d-md-block d-md-flex flex-row justify-content-between"]/div/span[2]/text()').extract()
        links = response.xpath('///div[@class="tupple_right_block d-none d-md-block"]/h3/a/@href').extract()
        link_list=[]
        for level in links:
            link_list.append(level.strip())
        data_dictionary = {'Name': schoolName_list, 'Course': course_list, 'Sector': sectors_list, 'Links ':link_list }
        
        df = pd.DataFrame.from_dict(data_dictionary, orient='index')
        df = df.transpose()

        df.to_csv('data_scrapy.csv', index = False, mode='a',header = False)
            
# run spider
process = CrawlerProcess()
process.crawl(careerSpider)
process.start()
df = pd.read_csv("data_scrapy.csv")
df = df.sort_values(by=['Name'], ascending=True)
df.to_csv('data_scrapy.csv', index = False)
