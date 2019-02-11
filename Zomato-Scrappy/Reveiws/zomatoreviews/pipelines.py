import csv
from items import Review
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import os

class MultiCSVItemPipeline(object):
    def __init__(self):
        self.files = {}
        if not os.path.exists(os.path.dirname('../../Results/Reviews/')):
            os.makedirs(os.path.dirname('../../Results/Reviews/'))

        f = open("cities.txt")
        cities = []
        #self.exporter = []
        self.exportcitymap = {} 
        for city in f.readlines():
           city = city.rstrip('\n')
           city = city.replace("/","_")
           myexport = CsvItemExporter(fields_to_export=Review.fields.keys(),file=open("../../Results/Reviews/Review_"+city+".csv",'w+'),delimiter='|')
           print ('CITY ',city)
           #self.exporter.append(myexport)
           self.exportcitymap[city] = myexport
        f.close()


      	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

    def spider_opened(self, spider):
        for export in self.exportcitymap:
          export.start_exporting()

    def spider_closed(self, spider):
        for export in self.exportcitymap:
           export.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        city = item['city']
        city = city.rstrip('\n')
        city = city.replace("/","_")
        self.exportcitymap[city].export_item(item)
        return item
        
        #names = Review().fields
        #self.csv_file = open('reviews.csv', 'w')
        #self.file = csv.DictWriter(self.csv_file, fieldnames=names,delimiter="|")
        #self.file.writeheader()

    #def process_item(self, item, spider):
    #    self.file.writerow(item)

    #def close_spider(self, spider):
    #    self.csv_file.close()

