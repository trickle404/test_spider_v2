import pymongo
import json
from itemadapter import ItemAdapter

class ParseDataPipeline:

    def __init__(self):
        self.proxies = []

    def process_item(self, item, spider):
        self.proxies.append(dict(item))

    def close_spider(self, spider):
        with open("proxies.json", "w", encoding="utf-8") as f:
            json.dump(self.proxies, f, ensure_ascii=False, indent=2)
