from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join
import unicodedata
import re

class Menu(Item):

   r_name = Field()
   city = Field()
   image_urls = Field()
   image_names = Field()
   images = Field()

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

class MenuItemLoader(ItemLoader):
    default_input_processor = MapCompose(unicode_convert)
    default_output_processor = TakeFirst()

    city_in = MapCompose(str.capitalize)


