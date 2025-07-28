import scrapy

class ParseDataItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    protocols = scrapy.Field()
    
