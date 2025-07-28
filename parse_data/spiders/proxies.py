import scrapy
import base64
from parse_data.items import ParseDataItem

class ProxiesSpyder(scrapy.Spider):
    name = "parse_proxy"
    start_urls = ["https://advanced.name/freeproxy"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = 1
        self.counts_proxies = 0
        self.max_limit = 150

    def parse(self, response):
        for row in response.css("tbody tr"):
            if self.counts_proxies >= self.max_limit:
                break
            item = ParseDataItem()
            item['ip'] = base64.b64decode(row.css("td[data-ip]::attr(data-ip)").get()).decode('utf-8')
            item['port'] = base64.b64decode(row.css("td[data-port]::attr(data-port)").get()).decode('utf-8')
            item['protocols'] = row.css('td:nth-child(4) a::text').getall()
            self.counts_proxies += 1
            yield item
        
        if self.counts_proxies < self.max_limit:
            self.page += 1
            next_page = f"https://advanced.name/freeproxy/?page={self.page}"
            yield response.follow(next_page, callback = self.parse)
