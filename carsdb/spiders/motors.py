import socket
import datetime
import scrapy
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from carsdb.items import CarsdbItem
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from dateutil.parser import parse
import re


class MotorSpider(scrapy.Spider):
    name = "motors"
    #allowed_domains = 'en.motors.com.mm'
    base_url = 'https://en.motors.com.mm'
    brands = ['Adixin', 'Audi', 'BAIC', 'Bajaj', 'BMW', 'Cadillac', 'Canda', 'Chevrolet',
      'Clark', 'CMC', 'Daihatsu', 'Demon', 'Dodge', 'Ducati', 'FAW', 'Ferrari', 'Ford',
      'Forland', 'Harley-Davison', 'Hino', 'Honda', 'Honda Motorcycles', 'Hummer',
      'Hyundai', 'Isuzu', 'Iveco', 'Jaguar', 'Jeep', 'Jialing', 'Jinbei', 'Kawasaki',
      'Kia', 'KTM', 'Land-Rover'
    ]  
    brands_test = ['BMW', 'Jeep']

    def start_requests(self):
        base_url = 'https://en.motors.com.mm'
        for b in self.brands_test:
            yield scrapy.Request(urljoin(base_url, b), 
                callback=self.parse_paging)
    

    def parse_paging(self, response):
        page_count = response.xpath('(//*[@class="pagination show-for-medium-up"][1]//a)[last()]/text()').extract()
        if len(page_count) == 0:
            page = 1
        else:
            page = int(page_count[0])
        for p in range(1, page+1):
            page_link = urljoin(str(response.url), '?sort=suggested&page='+str(p))
            yield scrapy.Request(page_link,callback=self.parse_items)
    

    def parse_items(self, response):
        detail_links = response.xpath('//*[@class="item-title type-m"][1]/a/@href').extract()
        for l in detail_links:
            yield scrapy.Request(urljoin(str(response.url),l), callback=self.parse_details)
        

    def parse_details(self, response):
        title = response.xpath('//*[@class="title-bar"][1]/span/text()').extract_first()
        price = response.xpath('//*[@class="type-xl"][1]/text()').extract_first()
        desc = response.xpath('//*[@class="description clearfix"][1]/p/text()').extract_first()
        submitted = response.xpath('//*[@class="submitted"][1]/span/text()').extract_first()
        fuel = response.xpath('//*[@class="column attribute"][3]/span/text()').extract_first()
        engine_power= response.xpath('//*[@class="column attribute"][4]/span/text()').extract_first()
        color = ""
        drive_type = ""
        doors = ""
        delar_name = response.xpath('//*[@class="left dealer-name"][1]//strong/text()').extract_first()

        l = ItemLoader(item=CarsdbItem(), response=response)
        l.add_xpath('title', '//*[@class="title-bar"][1]/span/text()')
        l.add_xpath('price', '//*[@class="type-xl"][1]/text()', 
            MapCompose(self.get_price, int))
        l.add_xpath('desc', '//*[@class="description clearfix"][1]/p/text()')
        l.add_xpath('submitted', '//*[@class="submitted"][1]/span/text()',
            MapCompose(self.get_date, str))
        l.add_xpath('fuel', '//*[@class="column attribute"][3]/span/text()')
        l.add_xpath('engine_power', '//*[@class="column attribute"][4]/span/text()',
            MapCompose(lambda i: i.strip().split()[0], int))
        l.add_xpath('dealer','//*[@class="left dealer-name"][1]//strong/text()')

        
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()

    # TODO: handle exception
    def get_price(self, value):
        result = 0
        try:
            postfix = value.strip().split(' ')[-1]
            result = int(postfix) * 100000
        except:
            result = 0
        
        return result

    def get_date(self, value):
        result = datetime.datetime.min
        try:
            result = parse(value.strip())
        except:
            result = datetime.datetime.min

        return result


    def remove_html(self, s):
        return re.sub(r"<[a-zA-Z0-9\"/=: ]+>", "", s)
