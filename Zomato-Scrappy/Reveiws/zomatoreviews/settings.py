SPIDER_MODULES = ['zomatoreviews.spiders']
NEWSPIDER_MODULE = 'zomatoreviews.spiders'
DEFAULT_ITEM_CLASS = 'zomatoreviews.items.Review'

ITEM_PIPELINES = {
 'zomatoreviews.pipelines.MultiCSVItemPipeline': 1000,
 }

DOWNLOADER_MIDDLEWARES = {
                         # 'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': None,
                         # 'scrapy.contrib.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
                         # 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
                         # 'random_useragent.RandomUserAgentMiddleware': 400,
                          'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
                          's3': None,
                         # 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware':None,
                         }
COOKIES_ENABLE = False
USER_AGENT_LIST="useragent.txt"
#LOG_LEVEL='DEBUG'
#LOG_FILE='review_debug.log'
