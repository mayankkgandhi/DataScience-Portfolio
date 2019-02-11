import scrapy
from scrapy.spiders import Spider
from re import findall
from zomatorestaurants.items import Restaurant
from zomatorestaurants.items import RestItemLoader
from random import randint
import random
from time import sleep

class ZomatoRestaurantSpider(Spider):
    name = 'zomatorestaurantspider'
    allowed_domains = ['zomato.com']
    #start_urls = [
    #    'https://www.zomato.com/chennai/restaurants?page=1'
        #'https://www.zomato.com/bangalore/restaurants?page=1',
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
        #rcity = findall('\\.com\/([a-z-/]+)\/', response.url)[0]
        rcity = response.url.rsplit('.com/', 1)[-1]
        index =rcity.find('/restaurants?page')
        if index == -1:
           index =rcity.find('?page')
        rcity = rcity[:index]

        for rest in response.css('a.result-title'):
            url = rest.xpath('@href').extract()[0]
            
            yield scrapy.Request(url, callback=self.parse_rest, meta={'rcity':rcity})
            
        sleep(random.uniform(0,3))
        next_link = response.css('li.current + li.active a').xpath('@href').extract()
        print "NEXT LINK:", next_link
        if next_link:
            yield scrapy.Request(response.urljoin(next_link[0]), callback=self.parse, meta={'rcity':rcity})

    def parse_rest(self, response):
        rest = RestItemLoader(item=Restaurant(), response=response)

        sleep(random.uniform(0,1))
        rest.add_xpath('r_name', '//h1/a/span/text()')
        rest.add_css('r_type', 'div.res-info-estabs > a::text')
        rest.add_value('r_url', response.url)
        rname = response.xpath('//h1/a/span/text()').extract()[0]
        rcity = response.meta['rcity']
        restid = (rcity+'/001/')+rname 
 
        rest.add_value('r_restid', restid)
        rest.add_css('r_cost', 'span[itemprop="priceRange"]::text')
        rest.add_css('r_location', 'span[itemprop="addressLocality"]::text')
        rest.add_css('r_rating', 'div[itemprop="ratingValue"]::text')
        rest.add_css('r_rating_votes', "span[itemprop='ratingCount']::text")
        rest.add_css('r_reviews', "div.res-main-stats-num::text")
        rest.add_css('r_photos', "div#ph_count::text")
        rest.add_css('r_bookmarks', "div#wtt_count::text")
        rest.add_css('r_checkins', "div#bt_count::text")
        rest.add_css('r_cuisines', "a[itemprop='servesCuisine']::text")
        rest.add_css('r_collections', "span.res-page-collection-text > a::text")
        rest.add_xpath('r_address', "//div[@class='res-main-address-text']/span//text()")
        latitude = response.css("meta[itemprop='latitude']").xpath('@content').extract()
        longtude = response.css("meta[itemprop='longitude']").xpath('@content').extract()
        rest.add_value('r_latitude', latitude)
        rest.add_value('r_longitude',longtude )
        rest.add_xpath('r_knownfor', '//div[@class="res-info-known-for-text mr5"]/text()')
        rest.add_css('r_payableby', 'span[itemprop="paymentAccepted"]::text')
        rest.add_xpath('r_speciala', '//div[@class="res-promo-text grey-data-icon"]/text()')
        rest.add_xpath('r_specialb', '//div[@class="mtop0 clearfix res-promo-dates"]/text()')
        rest.add_xpath('r_recommendeddishes', '//div[@class="res-info-dishes-text order-dishes"]/text()')
        rest.add_xpath('r_highlights','//div[@class="res-info-feature-text"]/text()')
	rest.add_css('r_payableby', 'span[itemprop="paymentAccepted"]::text')
        rest.add_xpath('r_openinghrs', '//div[@class="res-week-timetable"]//text()')
        rest.add_value('r_reviewpath',u'Results/Reviews/'+rcity)
        rest.add_value('r_blogpath', u'Results/Blogs/'+rcity)
        rest.add_value('r_menupath',u'Results/MenuStore/'+rcity+'_001_'+rname)
 
        yield rest.load_item()
