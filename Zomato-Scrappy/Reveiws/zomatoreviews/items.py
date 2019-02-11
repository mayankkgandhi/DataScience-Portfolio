from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join
import unicodedata
import re

class Review(Item):

    r_name = Field()
    r_url = Field()
    city = Field()
    popular = Field()
#    following = Field()
    reviewnum = Field()
    reviewername = Field()
    rest_review = Field()    
    reviewerurl = Field()
    noofreviewerrev = Field()
    nooffollower = Field()
    date = Field()
    rateofreview = Field()
    reviewtext = Field()

def unicode_convert(s):
    return unicodedata.normalize('NFKD', s).encode('utf8', 'ignore')

def int_convert(x):
    try:
        return int(x)
    except ValueError:
        return None

def float_convert(x):
    try:
        return float(x)
    except ValueError:
        return None

class ReviewItemLoader(ItemLoader):
    default_input_processor = MapCompose(unicode_convert)
    default_output_processor = TakeFirst()
    
    city_in = MapCompose(str.capitalize)
    noofreviewerrev_in = MapCompose(unicode.strip,int_convert)
    reviewnum_in = MapCompose(unicode.strip,int_convert)
         
    reviewtext_in = MapCompose(unicode.strip, unicode_convert)
    rateofreview_in = MapCompose(unicode.strip, float_convert)
        
