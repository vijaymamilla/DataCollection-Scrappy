import scrapy
from ..items import ClickBDItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class DataExtractionSpider(scrapy.Spider):
    name = "clickbd_spider"
    start_urls = ["https://www.clickbd.com/search?category=properties-and-rents"]
    website_main_url = "https://www.clickbd.com"

    #
    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        url_context_names = response.css("div.sh > a::attr(href)").getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]

        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        all_pages_links = response.css('ul.pagination li a::attr(href)').getall()

        if all_pages_links is not None:
            next_page = all_pages_links[-1]
            new_url = self.website_main_url+next_page
            print("[new_url]",new_url)
            yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)

    def parse_details_page(self, response):

        item = ClickBDItem()
        item['price'] = response.css('.item-price span::text').get()
        item['location'] = response.css('.delivery_info .row:nth-child(2) div.col-xs-9::text').get().strip()
        item['num_bed_rooms'] = response.css("div.col-md-12 li:nth-child(5)::text").get()
        item['num_bath_rooms'] = response.css("div.col-md-12 li:nth-child(6)::text").get()
        item['num_balconies'] = response.css('.col-md-12 li:nth-child(7)::text').get()
        item['area'] = response.css("div.col-md-12 ul li:nth-child(4)::text").get()
        item['building_height'] = response.css('div.col-md-12 li:nth-child(10)::text').get()
        item['car_parking'] = response.css('ul li:nth-child(8)::text').get()
        #item['units_floor'] = response.css('div.col-md-12 ul li:nth-child(10)::text').get().strip()
        item['building_height'] = response.css('div.col-md-12 ul li:nth-child(10)::text').get()
        # item['building_type'] = response.css("ul._033281ab li span._812aa185::text").get()
        # item['purpose'] = response.xpath('//span[contains(@aria-label, "Purpose")]/text()').get()
        # item['amenities'] = '##'.join(response.css('div._40544a2f span._005a682a::text').getall())
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