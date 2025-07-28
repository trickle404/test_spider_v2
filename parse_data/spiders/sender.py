import scrapy
import json

from scrapy.http import JsonRequest

class SenderSpider(scrapy.Spider):
    name = "sender"
    start_urls = ['https://test-rg8.ddns.net/api/get_token']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_url = "https://test-rg8.ddns.net/api/post_proxies"
        self.batch_size = 10
        self.max_batches = 15
        with open("proxies.json", "r", encoding="utf-8") as f:
            self.proxies = json.load(f)

        self.proxies_str_list = [f"{p['ip']}:{p['port']}" for p in self.proxies]

    def start_requests(self):
        yield scrapy.Request(
            url = "https://test-rg8.ddns.net/api/get_token",
            callback = self.parse,
            meta={'cookiejar': 1}
        )
    def parse(self, response):
            yield scrapy.Request(
                url=self.api_url,
                callback=self.post_proxies,
                meta={"cookiejar":1}
            )

    def post_proxies(self, response):
        for i in range(min(self.max_batches, (len(self.proxies_str_list) + self.batch_size -1) // self.batch_size)):
            batch = self.proxies_str_list[i*self.batch_size:(i+1)*self.batch_size]
            data = {
                "user_id" : "t_1363631d",
                "len" : self.batch_size,
                "proxies" : ", ".join(batch)
            }
            yield JsonRequest(
                url="https://test-rg8.ddns.net/api/post_proxies",
                data= {
                    "user_id" : "t_1363631d",
                    "len" : 10,
                    "proxies" : ", ".join(data)
                },
                callback=self.handle_response,
                errback = self.handle_erorr,
                meta={
                    'cookiejar': 1,
                    'batch' : batch,
                },
                dont_filter=True
            )
    
    def handle_response(self, response):
        if response and response.status == 429:
            ...

    def handle_erorr(self, response):
        self.logger.error(response)    
        