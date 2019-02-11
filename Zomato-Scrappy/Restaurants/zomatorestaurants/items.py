from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join
import unicodedata
import re

class Restaurant(Item):

    r_name = Field()
    r_restid = Field()
    r_type = Field()
    r_address = Field()
    r_city = Field()
    r_url = Field()
    r_cost = Field()
    r_location = Field()
    r_rating = Field()
    r_rating_votes = Field()
    r_reviews = Field()
    r_photos = Field()
    r_bookmarks = Field()
    r_checkins = Field()
    r_cuisines = Field()
    r_collections = Field()
    r_latitude = Field()
    r_longitude = Field()
    r_payableby = Field()
    r_highlights = Field()
    r_speciala = Field()
    r_specialb = Field()
    r_knownfor = Field()
    r_recommendeddishes = Field()
    r_openinghrs = Field()
    r_menupath = Field()
    r_blogpath = Field()
    r_reviewpath = Field()    

def unicode_convert(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

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


class RestItemLoader(ItemLoader):
    default_input_processor = MapCompose(unicode_convert)
    default_output_processor = TakeFirst()

#    r_restid_in = MapCompose(int_convert)

    r_url_in = Identity()

    r_city_in = MapCompose(str.capitalize)
    cost_in = MapCompose(unicode.strip, float_convert)

    r_rating_in = MapCompose(unicode.strip, float_convert)

    r_rating_votes_in = MapCompose(int_convert)
    r_reviews_in = MapCompose(int_convert)
    r_photos_in = MapCompose(int_convert)
    r_bookmarks_in = MapCompose(int_convert)
    r_checkins_in = MapCompose(int_convert)

    r_cuisines_out = Join(",")#Identity()
    r_collections_out = Join(",")#Identity()

    r_address_in = MapCompose(unicode.strip, unicode_convert)
#    r_address_out = MapCompose(

    r_latitude_in = MapCompose(float_convert)
    r_longitude_in = MapCompose(float_convert)

    r_payableby_out = Join(",")
    r_highlights_out = Join(",")
    
    r_knownfor_in = MapCompose(unicode.strip, unicode_convert)
    r_knownfor_out = Join(",")
    
    r_openinghrs_out = Join(",")
    
    r_recommendeddishes_in = MapCompose(unicode.strip, unicode_convert)    

    r_speciala_in = MapCompose(unicode.strip, unicode_convert)
   
    r_specialb_in = MapCompose(unicode.strip, unicode_convert)

    r_specialb_out = Join(" ") #Identity()#MapCompose(unicode.strip, unicode_convert)


