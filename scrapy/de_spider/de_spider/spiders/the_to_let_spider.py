import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..items import ThetoletItem


class CyborgSpider(scrapy.Spider):
    name = 'cyborg'

    start_urls = ['https://www.thetolet.com/en/property-listing']

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.maximize_window()
        count_2 = 0
        property_post_listing_urls = []

        for _ in range(0, 3):
            total_div = self.driver.find_elements(By.XPATH, '//*[@id="wrapper"]/div[4]/div/div[1]/div/div')
            count_2 = len(total_div)
            self.driver.execute_script("arguments[0].scrollIntoView();", total_div[-1])
            link = self.driver.find_element(By.XPATH,
                                            f'//*[@id="wrapper"]/div[4]/div/div[1]/div/div[{str(count_2)}]/div/div')
            # for i in range(count_2-30, count_2):
            #     property_post_listing_urls.append(
            #         response.xpath(f'//*[@id="wrapper"]/div[4]/div/div[1]/div/div[{str(i)}]/a').xpath('@href').get())

            link.click()
            time.sleep(5)

        # print(len(total_div))
        # property_post_listing_urls = response.css('div.listing-item a.listing-img-container::attr(href)').getall()

        # for i in range(1, count_2):
        #     property_post_listing_urls.append(
        #         response.xpath(f'//*[@id="wrapper"]/div[4]/div/div[1]/div/div[{str(i)}]/a').xpath('@href').get())
        for i in range(1, count_2):
            property_post_listing_urls.append(
                self.driver.find_element(By.XPATH, f'//*[@id="wrapper"]/div[4]/div/div[1]/div/div[{str(i)}]/a/@href'))

        for url in property_post_listing_urls:
            yield scrapy.Request(url=url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        property_specification_list = response.css('ul.property-main-features').get().replace('<li>', '').replace(
            '</li>\n',
            '').replace(
            '<ul class="property-main-features">\n', '').replace('<span>', ':').replace('</span>', ',').replace('</ul>',
                                                                                                                '').replace(
            ' ', '')[:-1] + ''

        item = ThetoletItem()
        item['property_specification'] = dict(
            item.split(':') for item in property_specification_list.split(','))  # converted to dict
        item['name'] = response.css('div.col-md-9 h2::text').get().replace('\n', '')
        item['price_per_month_BDT'] = response.css('div.property-price').get().replace(
            '<div class="property-price">\n<br>\n', '') \
            .replace('/- BDT </div>', '')

        address_list = response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/ul[3]//text()').getall()
        address_list_str = ''.join(address_list).strip("\n").replace('\n', ', ')  # converted to str

        item['address'] = address_list_str + ', ' + ' '.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/ul[2]//text()').getall()).strip("\n")
        item['rules'] = ''.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/ul[4]//text()').getall()).strip("\n").replace('\n',
                                                                                                                   ', ')
        item['description'] = ''.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/div[1]//text()').getall()).strip("\n").replace(
            '\n', ', ').replace('Show More', '').encode('utf-8')
        item['feature'] = ''.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/ul[6]//text()').getall()).strip('\n').replace('\n',
                                                                                                                   ',')

        yield item