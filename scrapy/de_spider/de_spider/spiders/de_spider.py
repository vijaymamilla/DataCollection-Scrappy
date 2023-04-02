import scrapy
from csv import writer

filename = 'output/housing.csv'


class DataExtractionSpider(scrapy.Spider):
    name = "de_spider"
    start_urls = ["https://www.bproperty.com/en/bangladesh/properties-for-sale/"]
    website_main_url = "https://www.bproperty.com/"
    header = "'Type', 'Location', 'Price', 'Area', 'Bed Rooms', 'Bath Rooms'"
    with open(filename, 'a+') as f:
        f.write(header + "\n")

    def parse(self, response):

        urls = response.css("li article div a._287661cb::attr(href)").getall()

        urls = [ self.website_main_url+context_name for context_name in urls]

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
        #yield  { "type":building_type,"location": location, "price":price, "area": area,"num_bed_rooms": num_bed_rooms, "num_bath_rooms":num_bath_rooms}


        with open(filename, 'a+') as f:
            f.write(info + "\n")
