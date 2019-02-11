from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from PIL import Image
from cStringIO import StringIO
import re

class MyImagesPipeline(ImagesPipeline):

    #CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')


    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict
    def get_media_requests(self, item, info):
        print "get_media_requests"
        return [Request(x, meta={'image_names': item["image_names"]})
                for x in item.get('image_urls', [])]

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        print "get_images"
        print ('request.url', request.url)
        for key, image, buf, in super(MyImagesPipeline, self).get_images(response, request, info):
            #if self.CONVERTED_ORIGINAL.match(key):
            key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):
        return "/%s.jpg" % response.meta['image_names'][0]


