from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from parse_data.spiders.proxies import ProxiesSpyder
from parse_data.spiders.sender import SenderSpider

def main():
    proccess = CrawlerProcess(get_project_settings())
    proccess.crawl(ProxiesSpyder)
    # proccess.crawl(SenderSpider)
    proccess.start()

if __name__ == "__main__":
    main()