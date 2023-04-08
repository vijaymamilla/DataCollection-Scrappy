import scrapy
from ..items import PBazarItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class PBazarExtractionSpider(scrapy.Spider):
    name = "pbazaar_spider"
    start_urls = ["https://pbazaar.com/en/search?TypeId=1&StateProvinceId=78&ThanaAreaId=0"]
    website_main_url = ['https://pbazaar.com/']

    #
    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        url_context_names = response.css('figure.col-md-6.image-holder a.property-featured-image::attr(href)').getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]
        print('URL_CONTEXT_NAMES     ', url_context_names, '  current_url_list    ', current_url_list)

        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        # next_page = response.xpath('//div/ul/li/a[contains(@title, "Next")]').xpath('@href').get()

        # if next_page is not None:

        #    new_url = self.website_main_url+next_page
        #    yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)

    def parse_details_page(self, response):

        item = PBazarItem()
        item['price'] = response.css("p.propertyHeader_heading::text").get()
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