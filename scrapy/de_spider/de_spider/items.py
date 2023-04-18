
from scrapy.item import Item, Field

class BpPropertyItem(Item):
    # define the fields for your item here like:
    price = Field()
    location = Field()
    num_bed_rooms = Field()
    num_bath_rooms = Field()
    area = Field()
    building_type = Field()
    purpose = Field()
    amenities = Field()
    property_url= Field()
    property_description = Field()
    property_overview = Field()
    commercial_type = Field()
    image_url = Field()

class PBazarItem(Item):

    location = Field()

class ClickBDItem(Item):
    price = Field()
    location= Field()
    num_bed_rooms = Field()
    num_bath_rooms = Field()
    num_balconies = Field()
    num_balconies = Field()
    area = Field()
    building_height = Field()
    car_parking = Field()
    #units_floor = Field()
    building_height = Field()

class BikroyItem(Item):
    price = Field()
    # location = Field()
    #num_bed_rooms = Field()
    #num_bath_rooms = Field()
    #area = Field()
    #building_type = Field()
    #purpose = Field()
    #amenities = Field()
    #property_url = Field()

class ThetoletItem(Item):
    location = Field()
    city = Field()
