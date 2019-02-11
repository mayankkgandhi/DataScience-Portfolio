import csv
from items import Restaurant
import os

class CSVPipeline(object):
    def __init__(self):
        names = Restaurant().fields
        local_filename = '../../Results/Restaurants/restaurants_profile.csv'
        if not os.path.exists(os.path.dirname(local_filename)):
            os.makedirs(os.path.dirname(local_filename))

        self.csv_file = open(local_filename, 'ab+')
        self.file = csv.DictWriter(self.csv_file, fieldnames=names,delimiter="|")
        self.file.writeheader()

    def process_item(self, item, spider):
        self.file.writerow(item)

    def close_spider(self, spider):
        self.csv_file.close()


