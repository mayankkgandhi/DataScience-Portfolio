import urllib2
import scrapy
import json
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy.spiders import Spider
from re import findall
from scrapy.selector import Selector
from zomatoreviews.items import Review
from zomatoreviews.items import ReviewItemLoader
# from scrapy import optional_features
# from pyvirtualdisplay import Display
from time import sleep
from random import randint
import random
from lxml import etree
import lxml.html

class ReviewSpider(Spider):
    name = 'reviewspider'
    allowed_domains = ['zomato.com']
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
    f = open("cities.txt")
    main_url = "https://www.zomato.com/"
    for city in f.readlines():
      city = city.strip()
      if city.endswith("restaurants"):
       start_urls.append(main_url+city.strip()+"?page=1")
       print("city is ", city)
      else:
       start_urls.append(main_url+city.strip()+"/restaurants?page=1")
    f.close()   
   
    def parse(self, response):
         rcity = response.url.rsplit('.com/', 1)[-1]
         index =rcity.find('/restaurants?page')
         if index == -1:
           index =rcity.find('?page')
         rcity = rcity[:index]
	 count = 0
         page_count = 1       
         rest = response.css('a[data-result-type="ResCard_Reviews"]')
         for restaurant in rest:
            url = restaurant.xpath('@href').extract()[0]
            print( "Parse: url: ", url)
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

            yield scrapy.Request(url, headers=header, callback=self.parse_reviews, meta={'rcity':rcity})
            sleep(random.uniform(0,2))
            #break    
    # currently scrapping only 1 page for test purpose. so commented below code
         # return
         
         print("Scrapping completed for Page No: ",page_count, " of city: ", rcity)
    # more through all pages and 
         next_link = response.css('li.current + li.active a').xpath('@href').extract()
         print "NEXT LINK:", next_link
         if next_link:
            page_count = page_count+1
            yield scrapy.Request(response.urljoin(next_link[0]), callback=self.parse,meta={'rcity':rcity})

            sleep(2)

    def parse_reviews(self, response):
       #try:  
         
         url= "https://www.zomato.com/php/social_load_more.php"
         rurl = response.url
         restname = response.xpath("//h1[@class='res-name left']/a/span/text()").extract()[0]
         elem_strreviewno = response.xpath('//a[@class="default-section-title everyone empty"]/span/text()').extract()
         if not elem_strreviewno:
              elem_strreviewno = response.xpath('//a[@class="default-section-title everyone active selected"]/span/text()').extract()
              if not elem_strreviewno:
                return
         strreviewno = elem_strreviewno[0]
         print('Number of reviews for url:" ',response.url ,' for ' ,restname ," ' is ", strreviewno)
         reviewno = int(strreviewno)
         if reviewno%5 == 0:
           page = (reviewno/5)-1
         else:
           page = (reviewno/5)
         
         rcity = response.meta['rcity']
         entity_id = response.xpath("//div[@class='clearfix zs-load-more res-page-load-more hidden']/attribute::data-entity_id").extract()[0]
         elem_noofpopular = response.xpath("//a[@class='default-section-title top active selected']/span/text()").extract()
         noofpopular  = 0
         if  elem_noofpopular:
            noofpopular = elem_noofpopular[0]
         #print entity_id
         reviewcount = 0
         for pg in range( 0, page+1):
           frmdata = {"entity_id":entity_id, "profile_action": "reviews-dd", "page": str(pg), "limit":"5"}
           yield FormRequest(url, callback=self.parse_allreviews, formdata=frmdata, meta = {'pageno': pg, 'reviewno':strreviewno, 'restname':restname, 'noofpopular':noofpopular, 'rcity': rcity, 'rurl': rurl })
 	
    def parse_allreviews(self,response):
       #try:    
         
         item=Review() 
         #doc = driver.page_source
         #tree = etree.HTML(doc)
         string = response.body.decode('utf-8')
         json_obj = json.loads(string)
         purehtml = json_obj['html'] 
#         print( 'response',purehtml)
         tree = lxml.html.fromstring(purehtml)
         #elem_restname = tree.xpath("//h1[@class='res-name left']/a/span")[0]
         #noofreview = tree.xpath("//a[@class='default-section-title everyone empty active selected']/span")[0].text
         print ('fullmeta',response.meta)
         item['r_name'] = response.meta['restname']
         item['r_url'] = response.meta['rurl'].rsplit('/',1)[0]
         rcity = response.meta['rcity']
         item['city'] = rcity
         pageno = response.meta['pageno']
         noofreview = response.meta['reviewno']
         totalrevscrapped = 0
         noofpopular = response.meta['noofpopular']
         elems_rname  = tree.xpath("//span[@class='h-level4 zblack']")
         elems_url = tree.xpath("//a[@class='snippet__link']")
         elems_noofreviews = tree.xpath("//span[@class='snippet__reviews']")
         elems_nooffollowers = tree.xpath("//span[@class='snippet__followers']")
         elems_date = tree.xpath("//a[@class='res-review-date']/time")
#         elems_reviewrate = tree.xpath("//div[contains(@class, 'ttupper fs12px left bold zdhl2 tooltip icon-font-level-2')]")
        
         curr_revno = (int(pageno)-1)*5
         if int(pageno) == 0:
           curr_revno = 0
         for rev_no in range(0, 5):  #number of times load more events to fired
           print("url :", response.request.url , " fetching review no: ",rev_no+1)
           curr_revno = curr_revno +1
           item['reviewnum'] = curr_revno
           item['rest_review'] = noofreview
           item['popular'] = noofpopular
           try:
            item['reviewername'] = elems_rname[rev_no].text      
           except:
            print("URL: ",response.url, " failed for reviewername on REVIEW_NO: ",str(curr_revno+1))
            continue
           try:
             item['reviewerurl'] = elems_url[rev_no].attrib["href"] 
           except:
             print("Restaurant: ",response.meta['restname']," failed for reviewerurl on REVIEW_NO: ",str(curr_revno+1))
             pass           
           try:
             item['noofreviewerrev'] = elems_noofreviews[rev_no].text
           except:
             print("Restaurant: ",response.meta['restname'], " failed for noofreviewers review on REVIEW_NO: ",str(curr_revno+1))
             pass
           try:
             item['nooffollower'] = elems_nooffollowers[rev_no].text
           except:
             print("Restaurant: ",response.meta['restname'], " failed for nooffollowers on REVIEW_NO: ",str(curr_revno+1))
             pass
           try:
             item['date'] = elems_date[rev_no].attrib['datetime']
           except:
             print("Restaurant: ",response.meta['restname'], " failed for date on REVIEW_NO: ",str(curr_revno+1))
             pass
           try:
             elem = tree.xpath("//div[@class='res-review-body clearfix']")
             elems_reviewrate =elem[rev_no].xpath(".//div[@class='rev-text']/div")
             if not elems_reviewrate:
                 elems_reviewrate =elem[rev_no].xpath(".//div[@class='rev-text hidden']/div")
             item['rateofreview'] = elems_reviewrate[0].attrib['aria-label']
           except:
             print("Restaurant: ",response.meta['restname'], " failed for date on REVIEW_NO: ",str(curr_revno+1))
             pass

           try:
             elems_review = tree.xpath("//div[@class='res-review-body clearfix']")
             elems_reviewtext = elems_review[rev_no].xpath(".//div[@class='rev-text']")
             if not elems_reviewtext:
               elems_reviewtext = elems_review[rev_no].xpath(".//div[@class='rev-text hidden']")
             revTextarray = elems_reviewtext[0]
             revText= " ".join([t.strip() for t in revTextarray.itertext()])
             revText = revText.lstrip(' ')

             if revText.startswith("Rated"):
                revText = revText[len("Rated"):]
             revText = revText.split('Like', 1)[0]
             revText = " ".join(revText.split())
             item['reviewtext'] = revText.encode('utf8')
           except:
             print("Restaurant: ",response.meta['restname'], " failed for reviewtext on REVIEW_NO: ",str(curr_revno+1))
             pass

           yield item
           totalrevscrapped = totalrevscrapped + 1
         print("Restaurant: ",response.meta['restname'], " Number of review scrapped: " , str(totalrevscrapped),'\n')             

       #except:   
        # print("ERROR: something went wrong in url: ",response.url)
        #display.stop()
        # pass

