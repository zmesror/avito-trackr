# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

class AvitoscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Convert published_date to datetime
        date = adapter["published_date"]
        adapter["published_date"] = self._to_datetime(date)

        return item
    
    def _to_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
