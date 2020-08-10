# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ClockItem(scrapy.Item):
    # define the fields for your item here like:
    product_code = scrapy.Field()
    product_name_from_official = scrapy.Field()
    prod_model = scrapy.Field()
    brand_en = scrapy.Field()
    prod_currency = scrapy.Field()
    price = scrapy.Field()
    prod_detail_link = scrapy.Field()
    prod_img_url = scrapy.Field()
    prod_case_meterial = scrapy.Field()
    prod_string_meterial = scrapy.Field()
    prod_movement = scrapy.Field()
    product_info = scrapy.Field()
    pass


class ShopItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field()
    product_code = scrapy.Field()
    parent_product_code = scrapy.Field() # 같은 제품에서 다른 색상일 경우, 부모 코드는 동일하게 갖음 보통.
    prod_img_url = scrapy.Field()
    prod_img_cnt = scrapy.Field()
    product_name_from_official = scrapy.Field()
    prod_color = scrapy.Field()
    price = scrapy.Field()
    prod_material = scrapy.Field()
    size_w = scrapy.Field()
    size_h = scrapy.Field()
    size_d = scrapy.Field()
    w_of_h = scrapy.Field()
    country = scrapy.Field()
    product_info = scrapy.Field()
    prod_detail_link = scrapy.Field()
    # for json
    category = scrapy.Field()
    pass