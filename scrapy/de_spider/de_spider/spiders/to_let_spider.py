import scrapy
from ..items import ThetoletItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class BikroySpider(scrapy.Spider):
    name = "tolet_spider"

    start_urls = ["https://www.thetolet.com/en/property-listing"]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        url_context_names = response.css("div.listings-container div.listing-item a.listing-img-container::attr(href)").getall()
        current_url_list = [ context_name for context_name in url_context_names]
        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)
        # next_page = response.xpath('//div/ul/li/a[contains(@title, "Next")]').xpath('@href').get()
        # if next_page is not None:
        #     new_url = self.website_main_url+next_page
        #     yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)

    def parse_details_page(self, response):
        item = ThetoletItem()
        tag = response.xpath('string(//span[@class="post-loc"]/a[@class="listing-address"])').get()
        address = tag.strip().split(',')
        item['location'] = address[0]
        item['city'] = address[1].strip()

        yield item

    def errback_httpbin(self, failure):
        # logs failures
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)