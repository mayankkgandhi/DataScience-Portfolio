SPIDER_MODULES = ['zomatorestaurants.spiders']
NEWSPIDER_MODULE = 'zomatorestaurants.spiders'
DEFAULT_ITEM_CLASS = 'zomatorestaurants.items.Restaurant'

ITEM_PIPELINES = {
 'zomatorestaurants.pipelines.CSVPipeline': 1000
 }

DOWNLOADER_MIDDLEWARES = {
                          'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
                          'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': None,
                          'scrapy.contrib.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
                          'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
                          's3': None,
                          'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware':None,
                         }
COOKIES_ENABLE = False
