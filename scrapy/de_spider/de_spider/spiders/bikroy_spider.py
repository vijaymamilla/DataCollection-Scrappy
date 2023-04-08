import scrapy
from ..items import BikroyItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class BikroySpider(scrapy.Spider):
    name = "bikroy_spider"

    start_urls = ["https://bikroy.com/en/ads/dhaka/property"]
    website_main_url = "https://www.bikroy.com"

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        url_context_names = response.css("ul.list--3NxGO a.card-link--3ssYv::attr(href)").getall()
        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]
        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)
        # next_page = response.xpath('//div/ul/li/a[contains(@title, "Next")]').xpath('@href').get()
        # if next_page is not None:
        #     new_url = self.website_main_url+next_page
        #     yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)

    def parse_details_page(self, response):
        item = BikroyItem()
        item['price'] = response.css("div.section--PpGYD div.money-section--fSWWQ  div.amount--3NTpl::text").get()
        #item['location'] = response.css("div.word-break--2nyVq value--1lKHt::text").get()
        #item['num_bed_rooms'] = response.css("div.word-break--2nyVq value--1lKHt::text").get()
        #item['num_bath_rooms'] = response.css("div.word-break--2nyVq value--1lKHt::text").get()
        #item['area'] = response.css("div.word-break--2nyVq value--1lKHt::text").get()
        #item['building_type'] = response.css("ul._033281ab li span._812aa185::text").get()
        #item['purpose'] = response.xpath('//span[contains(@aria-label, "Purpose")]/text()').get()
        #item['amenities'] = '##'.join(response.css('div._40544a2f span._005a682a::text').getall())
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