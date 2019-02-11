SPIDER_MODULES = ['zomatomenus.spiders']
NEWSPIDER_MODULE = 'zomatomenus.spiders'
DEFAULT_ITEM_CLASS = 'zomatomenus.items.Menu'

ITEM_PIPELINES = {'zomatomenus.pipelines.MyImagesPipeline': 1}

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

IMAGES_STORE = 'MenuStore'
