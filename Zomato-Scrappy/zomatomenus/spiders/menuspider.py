import urllib
import scrapy
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy.spiders import Spider
from re import findall
from scrapy.selector import Selector
from zomatomenus.items import Menu
from zomatomenus.items import MenuItemLoader
from scrapy import optional_features
from pyvirtualdisplay import Display
from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.proxy import *
import os
#optional_features.remove('boto')


class MenuSpider(Spider):
    name = 'menuspider'
    allowed_domains = ['zomato.com']
    # currently scrapping only 1 page for test purpose. so commented below code

    #start_urls = [
    #    'https://www.zomato.com/bangalore/restaurants?page=1',
        #'https://www.zomato.com/mysore/restaurants?page=1',
        #'https://www.zomato.com/pune/restaurants?page=1',
        #'https://www.zomato.com/mumbai/restaurants?page=1',
        #'https://www.zomato.com/hyderabad/restaurants?page=1',
        #'https://www.zomato.com/kolkata/restaurants?page=1',
        #'https://www.zomato.com/ncr/restaurants?page=1',
    #]
    start_urls = []
    input_file = "cities.txt"
    #if not os.path.exists(os.path.dirname(input_file)):
    #   print("No input file for Cities exist")
    #   os.makedirs(os.path.dirname(input_file))
             

    f = open(input_file)
    main_url = "https://www.zomato.com/"
    for city in f.readlines():
      city = city.strip()
      if city.endswith("restaurants"):
       start_urls.append(main_url+city.strip()+"?page=1")
       print("city is ", city)
      else:
       start_urls.append(main_url+city.strip()+"/restaurants?page=1")
    f.close()


    def __init__(self):
        #create a instance of the selenium webdriver using Firefox and assign it to the 'driver' instance variable.
        self.driver = webdriver.Firefox()

    def close(self, spider):
        self.driver.quit()

    def spider_detail(self, spider):
        self.driver.close()


    def parse(self, response):
         #rcity = findall('\\.com\/([a-z-/]+)\/', response.url)[0]
         rcity = response.url.rsplit('.com/', 1)[-1]
         index =rcity.find('/restaurants?page')
         if index == -1:
           index =rcity.find('?page')
         rcity = rcity[:index]

         count = 0
         menus = response.css('a[data-result-type="ResCard_Menu"]')
         for menu in menus:
            url = menu.xpath('@href').extract()[0]
            header = {
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Host': 'www.zomato.com',
                   'Accept':'*/*',
                   'Accept-Encoding':'gzip, deflate,br',
                   'Referer':'https://www.zomato.com',
                   #'Content-Length':'57',
                   'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                   'dont_filter':'True' }

            yield scrapy.Request(url, headers=header,callback=self.parse_allreview,meta={'rcity':rcity})
            #print("url: ", url , " scrapped ",'\n')
            sleep(random.uniform(0,2))
            #break
            
    # more through all pages and 
         next_link = response.css('li.current + li.active a').xpath('@href').extract()
         print "NEXT LINK:", next_link
         if next_link:
           yield scrapy.Request(response.urljoin(next_link[0]), callback=self.parse,meta={'rcity':rcity})
           sleep(random.uniform(0,3))

    def parse_allreview(self, response):
       #try:   
         query_page = 0
         #url= 'https://www.zomato.com/php/social_load_more.php'
         
         #print ("response = ",response.body)

         driver = self.driver
         driver.get(response.url)
         
         pageno = driver.find_elements_by_xpath("//div[@class='pagination-meta left']/div")[0].text
         
         maxpage = 1
         if pageno.startswith('Page 1 of '):
           maxpage = int( pageno[len('Page 1 of '):])
         else:
           pass

         item = Menu()
         elem = driver.find_elements_by_xpath("//h1[@class='res-name left']/a/span")[0]
         r_name = elem.text
         city = response.meta['rcity']

         for offset in range(1, maxpage+1):  #number of times next page to fired

             # scrap the currrent image first
             link = driver.find_elements_by_xpath("//div[@id='menu-image']/img")[0].get_attribute('src')
             #local_filename = city+"_001_"+r_name+"_menu_"+str(offset)

             local_filename = "../../Results/MenuStore/"+city+"_001_"+r_name+"/menu_"+str(offset)
             if not os.path.exists(os.path.dirname(local_filename)):
                os.makedirs(os.path.dirname(local_filename))
             urllib.urlretrieve(link, local_filename)
  
             #item['image_urls'].append(link)
             #item['image_names'].append(item['r_name']+"_001_"+item['r_name_']+"menu-"+str(offset))
             if offset > maxpage:
               break
             loadmores = driver.find_elements_by_xpath("//a[@id='menu-next-page']")
             

             if not loadmores:
               break
             loadmorebtn = loadmores[0]
             loadmorebtn.click()
             wait = WebDriverWait(driver, 3)
         print("url:", response.request.url," next-page clicked ",offset, "times")
         #yield item
         return 
             #break
         



         
