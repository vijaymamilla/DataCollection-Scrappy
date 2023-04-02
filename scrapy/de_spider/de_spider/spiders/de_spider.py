import scrapy
from csv import writer

filename = 'output/housing.csv'


class DataExtractionSpider(scrapy.Spider):
    name = "de_spider"
    start_urls = ["https://www.bproperty.com/en/bangladesh/properties-for-sale/"]
    website_main_url = "https://www.bproperty.com/"
    header = "'Type', 'Location', 'Price', 'Area', 'Bed Rooms', 'Bath Rooms'"

    def parse(self, response):

        listed_items = response.css("li article div a._287661cb::attr(href)")
        urls = []

        for item in listed_items :
            context_name = item.get()
            urls.append(f"{self.website_main_url}{context_name}")

        with open(filename, 'a+') as f:
             f.write(self.header + "\n")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_details_page)

    def parse_details_page(self, response):

        price = response.css("span._105b8a67::text").get()
        location = response.css("div._1f0f1758::text").get()
        num_bed_rooms = response.css("span.fc2d1086::text").get()
        num_bath_rooms = response.css("span.fc2d1086::text").get()
        area = response.css("span.fc2d1086::text").get()
        building_type = response.css("span._812aa185::text").get()

        info = f"{building_type}, {location}, {price}, {area}, {num_bed_rooms}, {num_bath_rooms}"

        with open(filename, 'a+') as f:
             f.write(info + "\n")
