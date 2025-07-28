import time
import scrapy
import json

from scrapy.http import JsonRequest
from twisted.internet.error import TimeoutError, DNSLookupError
from twisted.web._newclient import ResponseFailed
from scrapy.spidermiddlewares.httperror import HttpError

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
                    "proxies" : ", ".join(batch)
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

        if response.status in (429, 403):
            time.sleep(30)
            yield scrapy.Request(
                url=self.start_urls[0],
                callback=self.parse,
                meta={'cookiejar': 1},
                dont_filter=True
            )
            return

        yield JsonRequest(
            url=response.url,
            data=json.loads(response.request.body.decode()),
            callback=self.handle_response,
            errback=self.handle_erorr,
            headers=response.request.headers,
            meta=response.meta,
            dont_filter=True
        )

    def handle_erorr(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HttpError on {response.url} — {response.status}")
            self.logger.error(f"Response body: {response.text}")

        elif failure.check(TimeoutError, DNSLookupError, ResponseFailed):
            self.logger.error(f"Network error: {failure.value}") 
        