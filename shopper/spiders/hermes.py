# -*- coding: utf-8 -*-
import scrapy
from shopper.items import ShopItem
import re
import traceback
import requests
import json

cookie_value = '_cs_c=1; _ga=GA1.2.86434885.1582704333; _fbp=fb.1.1582704333308.1437445694; _gcl_au=1.1.1507527297.1590654980; ABTasty=uid=jvx0088w06ktk3yv&fst=1582704333216&pst=1582704333216&cst=1591235066623&ns=2&pvt=13&pvis=13&th=; _cs_id=da07c3fd-dde9-a1c5-fb8d-dcaff1f162f7.1582704333.19.1595486995.1595486995.1.1616868333192.Lax.0; _gid=GA1.2.1206130999.1596419374; ECOM_SESS=ricmkl7b0q13v8p48ka8lm0s95; _cs_mk=0.9219878928930292_1596433456487; _gat_UA-72839523-2=1; _gat_UA-64545050-1=1; _dc_gtm_UA-72839523-2=1; _dc_gtm_UA-64545050-1=1; datadome=CwwuhAW68OqgmH0U5UZq-xMOWPH3IPgRbLDr-1ZmnPImDaDx5z1F0BJJbaaUgRxyKBbAXTw.gXdH2GVeVjVJW8NjRlcVU5f2Gq7ONeAKII'
headers = {
    'Cookie': cookie_value,
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}


class HermesSpider(scrapy.Spider):
    # Spider 객체를 식별하는 역할을 하는 클래스 변수
    name = 'HERMES'
    alias = 'he'

    allowed_domains = ['www.hermes.com', 'bck.hermes.com']
    start_urls = ['https://www.hermes.com/kr/ko/']

    # Secondhands 내부 id 생성을 위한 규칙
    categoryId = "A"
    brandId = "06"
    fromId = "01"

    def start_requests(self):
        # # 테스트용
        # url = 'https://www.hermes.com/kr/ko/product/roulis-verso-%EB%AF%B8%EB%8B%88-%EB%B0%B1-H079099CKAC/'
        # request = scrapy.Request(url=url, callback=self.parse_detail)
        # yield request
        # return

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        self.logger.info('URL: {:} '.format(response.url))
        sub_cate = response.xpath('//ul[contains(@class, "nav-list-menu")]')

        # 여성 >
        cate_bags = sub_cate.xpath('./li[span="여성"]/ul/li[span="가방과 가죽소품"]//li')

        # for cate in cate_bags:
        cate = cate_bags[2] # for test
        cate_name = cate.xpath('./a/text()').extract_first().strip()
        cate_link = cate.xpath('./a/@href').extract_first()

        # print(cate_name, cate_link)
        request = scrapy.Request(url="https://" + self.allowed_domains[0] + cate_link, callback=self.parse)
        request.meta['category'] = cate_name
        yield request

    def parse(self, response):
        self.logger.info('URL: {:} '.format(response.url))
        # item_list = response.xpath('//div[@class="grid-results"]//ul[@id="grid-results-ul"]/li')

        # headers = {
        #     'Cookie': 'datadome=HxvGzQAjfIfWUxtqwWvVTMJBx50fjxbtXrqdufvTcS9lHwts0sRgO3efWlL2ZSMWSIwS4oy0nPsYCJLnWhPzl9gg8PJazgBPT07N7UQajO',
        #     # 'Cache-Control': 'no-cache',
        #     'Accept': '*/*',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        # }

        cate_text = response.xpath('//li[contains(@class, "filter-checkbox-wrapper")]/button/@value').extract_first()
        cate_text_list = cate_text.split("categories")[1].split('%7d%2f')[0].split('_')
        param_category = cate_text_list[len(cate_text_list)-1]
        pagesize = 108  # todo
        url = f'https://bck.hermes.com/product?locale=kr_ko&category={param_category}&sort=relevance&pagesize={pagesize}'

        self.logger.info('URL: {:} '.format(url))
        url_response = requests.get(url, headers=headers)
        res_json = url_response.json()

        products = res_json["products"]
        item_list = products["items"]

        # url = 'https://www.hermes.com/kr/ko/product/roulis-verso-%EB%AF%B8%EB%8B%88-%EB%B0%B1-H079099CKAC/'
        # url = 'https://www.hermes.com/kr/ko/product/carre-pocket-%EB%9E%9C%EC%95%BC%EB%93%9C-H077726CKAA'
        # url = 'https://www.hermes.com/kr/ko/product/roulis-verso-미니-백-H079099CKAC/'
        # url = 'https://www.hermes.com/kr/ko/product/verrou-chaine-%EB%AF%B8%EB%8B%88-%EB%B0%B1-H071320CKX9/'
        # request = scrapy.Request(url=url, callback=self.parse_detail)
        # yield request

        for item in item_list:
            link = item["url"]
            if link is None:
                continue

            link = "https://"+self.allowed_domains[0] + "/kr/ko" + link.strip() + "/"
            # self.logger.info('DETAIL PAGE URL: {:} '.format(link))
            request = scrapy.Request(url=link, callback=self.parse_detail, headers=headers)
            request.meta['category'] = response.meta['category']
            yield request

    # 상세페이지 파싱
    def parse_detail(self, response):
        self.logger.info('URL: {:} '.format(response.url))

        m_item = ShopItem()
        product_info = ""

        try:
            product_detail = response.xpath('//div[@class="product-infos"]')
            # detail_link
            m_item['prod_detail_link'] = response.url

            # for json
            if "category" in response.meta:
                m_item['category'] = response.meta['category']
            else:
                self.logger.error(f'NO CATECORY >>  {response.url}')

            # product_code
            code = product_detail.xpath('.//p[contains(@class, "product-sku")]/text()').extract_first()
            if code:
                product_info += f"{code} / "
                code = code.split("제품 번호:")[1].strip()
                m_item['product_code'] = code

                # parent_product_code
                code_group = code[0:7]      # product_code의 앞7자리
                m_item['parent_product_code'] = code_group
            else:
                self.logger.error(f'[CRAWL] NO PRODUCT CODE >>  {response.url}')

            # 다른 색상 제품
            other_colors = response.xpath('//ul[@class="product-configurator-form-options"]/li/label/@data-sku').extract()
            for other in other_colors:
                product_code = other.strip()
                if product_code == code:
                    continue
                url = f'https://bck.hermes.com/product-page?locale=kr_ko&productsku={product_code}'
                # url_response = requests.get(url, headers=headers)
                # contents = url_response.json()
                request = scrapy.Request(url=url, callback=self.parse_detail_other, headers=headers)
                request.meta['category'] = response.meta['category']
                yield request

            # product_name_from_official
            title = product_detail.xpath('.//p[@class="product-title"]/text()').extract_first()
            if title:
                m_item['product_name_from_official'] = title.strip()
            else:
                self.logger.error(f'No title here >>  {response.url}')

            # price
            price = product_detail.xpath('.//p[@class="product-price"]/text()').extract_first()
            if price:
                product_info += price.strip() + " / "
                price = price.replace("₩", "").replace(",", "")
                m_item['price'] = price.strip()
            else:
                self.logger.error(f'No price here >>  {response.url}')

            # prod_color
            color = product_detail.xpath('.//h4//span[contains(@class, "toggler-text")]/text()').extract_first()
            if color:
                m_item['prod_color'] = color.strip()
            else:
                self.logger.error(f'No color here >>  {response.url}')

            # 상세설명
            description = product_detail.xpath('.//p[@class="product-attribute-font-description"]/text()').extract()
            if description:
                for desc in description:
                    desc = desc.strip()
                    product_info += desc + " / "
            else:
                self.logger.error(f'No description here >>  {response.url}')

            # 제품 세부 정보
            product_toggles = product_detail.xpath('.//div[@class="product-toggles"]')
            detail_info = product_toggles.xpath('./h-toggle[@id="product-toggle-productDetail"]')
            detail_info_content = ""
            detail_info_content_strong = detail_info.xpath('.//div[@role="region"]//strong/text()').extract_first()
            detail_info_content_p = detail_info.xpath('.//div[@role="region"]//p/text()').extract()
            detail_info_title = product_toggles.xpath('.//span[contains(@class, "toggle-header-text")]/text()').extract_first()

            if detail_info_content_strong:
                detail_info_content += detail_info_content_strong
                # prod_material
                material = detail_info_content_strong.strip().split(" ")[0]
                if material:
                    m_item['prod_material'] = material.strip()
                else:
                    self.logger.error(f'No material here >>  {response.url}')

            if detail_info_content_p:
                for p in detail_info_content_p:
                    detail_info_content += p

            if detail_info_title:
                detail_info_title = detail_info_title.strip() + '\n'
            if detail_info_content:
                product_info += detail_info_title + detail_info_content + " / "
            else:
                self.logger.error(f'No detail info here >>  {response.url}')

            # size cm 단위로 w, h, d (길이, 높이, 너비)
            size_group = product_detail.xpath('.//p[@class="product-attribute-font-description ng-star-inserted"]/text()').extract_first()
            try:
                product_info += size_group + " / "
                size_group = size_group.split("크기:")[1]
                size_info = size_group.replace("L", "").replace("H", "").replace("D", "").replace("cm", "").split('x')
                m_item['size_w'] = size_info[0].strip()
                m_item['size_h'] = size_info[1].strip()
                m_item['size_d'] = size_info[2].strip()

                m_item['w_of_h'] = float(m_item['size_w']) / float(m_item['size_h'])
            except:
                self.logger.error('Exception in size_info :: \n{:}'.format(traceback.format_exc()))

            # 제조국
            description = product_detail.xpath('.//p[@class="product-attribute-font-description"]/text()').extract()
            if description:
                country = ""
                for desc in description:
                    if desc.find("제조") != -1:
                        country = desc.split("제조")[0].strip()   # 마지막 제조 앞단어를 제조국으로 사용
                if country:
                    m_item['country'] = country
                else:
                    self.logger.error(f'No country here >>  {response.url}')
            else:
                self.logger.error(f'No country here >>  {response.url}')

            # 스토리 비하인드
            story_behind_title = response.xpath('//h2[@class="editorial-block-title"]/text()').extract_first()
            story_behind = response.xpath('//p[@class="editorial-block-text"]/text()').extract_first()
            if not story_behind:
                story_behind = response.xpath('//p[@class="editorial-block-intro"]/text()').extract_first()

            if story_behind_title:
                story_behind_title = story_behind_title.strip() + '\n'
            if story_behind:
                product_info += (story_behind_title + story_behind.strip())
            else:
                self.logger.error(f'No story behind here >>  {response.url}')

            # thumbnail
            m_item['prod_img_url'] = []
            image_list = response.xpath('//div[contains(@class, "gallery-container")]/button/img/@src').extract()
            if image_list:
                for image in image_list:
                    full_img_url = 'https:' + image
                    m_item['prod_img_url'].append(full_img_url.strip())
            else:
                self.logger.error(f'No image here >>  {response.url}')
            m_item['prod_img_cnt'] = len(m_item['prod_img_url'])

            m_item['product_info'] = product_info

        except:
            m_item['product_info'] = product_info
            self.logger.error('Exception in parse-detail:: \n{:}'.format(traceback.format_exc()))

        yield m_item

    def parse_detail_other(self, response):
        self.logger.info('URL: {:} '.format(response.url))

        m_item = ShopItem()
        product_info = ""

        try:
            # detail_link
            m_item['prod_detail_link'] = response.url

            # for json
            if "category" in response.meta:
                m_item['category'] = response.meta['category']
            else:
                self.logger.error(f'NO CATECORY >>  {response.url}')

            str_result = response.text
            str_result = str_result.replace("'", "\"")  # single quote to double quote
            response = json.loads(str_result)

            # product_code
            if "sku" in response:
                code = response["sku"]
                m_item['product_code'] = code

                # parent_product_code
                code_group = code[0:7]      # product_code의 앞7자리
                m_item['parent_product_code'] = code_group
            else:
                self.logger.error(f'[CRAWL] NO PRODUCT CODE >>  {response.url}')

            # product_name_from_official
            if "title" in response:
                title = response["title"]
                m_item['product_name_from_official'] = title
            else:
                self.logger.error(f'No title here >>  {response.url}')

            # price
            if "price" in response:
                m_item['price'] = response["price"]
            else:
                self.logger.error(f'No price here >>  {response.url}')

            if "simpleAttributes" in response:
                simpleAttributes = response["simpleAttributes"]

                # prod_color
                if "colorHermes" in simpleAttributes:
                    m_item['prod_color'] = simpleAttributes["colorHermes"]
                else:
                    self.logger.error(f'No color here >>  {response.url}')
                # 상세설명, 제조국
                if "description" in simpleAttributes:
                    description = simpleAttributes["description"]
                    product_info += description + " / "
                    desc_list = description.split("<br />")
                    country = desc_list[len(desc_list)-1].split(" ")[0]
                    m_item['country'] = country
                else:
                    self.logger.error(f'No description & country here >>  {response.url}')

                # size
                if "dimensions" in simpleAttributes:
                    size_group = simpleAttributes["dimensions"]
                    product_info += size_group + " / "
                    size_group = size_group.split("크기:")[1]
                    size_info = size_group.replace("L", "").replace("H", "").replace("D", "").replace("cm", "").split('x')
                    m_item['size_w'] = size_info[0].strip()
                    m_item['size_h'] = size_info[1].strip()
                    m_item['size_d'] = size_info[2].strip()
                    m_item['w_of_h'] = float(m_item['size_w']) / float(m_item['size_h'])
                else:
                    self.logger.error(f'No size here >>  {response.url}')
            else:
                self.logger.error(f'No simpleAttributes here >>  {response.url}')

            # 제품 세부 정보, prod_material, 스토리 비하인드
            if "content" in response and "toggles" in response["content"]:
                content = response["content"]
                toggles = content["toggles"]

                if "product_detail" in toggles:
                    product_detail = toggles["product_detail"]

                    product_detail_title = toggles["product_detail_title"]
                    product_info += product_detail_title + "\n" + product_detail + " / "

                    material = product_detail.split("<strong>")[1].split(" ")[0]
                    if material:
                        m_item['prod_material'] = material.strip()
                    else:
                        self.logger.error(f'No material here >>  {response.url}')
                else:
                    self.logger.error(f'No detail info, prod_material here >>  {response.url}')

                # 스토리 비하인드
                if "story_behind" in content and "content" in content["story_behind"]:
                    story_behind = content["story_behind"]

                    story_content = story_behind["content"]

                    if story_content.find("<p class=\"editorial-block-text\">") != -1:
                        story_text = story_content.split("<p class=\"editorial-block-text\">")[1].split("</p>")[0]
                    elif story_content.find("<p class=\"editorial-block-intro\">") != -1:
                        story_text = story_content.split("<p class=\"editorial-block-intro\">")[1].split("</p>")[0]
                    else:
                        story_text = ""

                    if story_text:
                        product_info += ("스토리 비하인드\n" + story_text.strip())

                else:
                    self.logger.error(f'No story behind here >>  {response.url}')
            else:
                self.logger.error(f'No detail info, prod_material, story behind here >>  {response.url}')

            print('hi')
            # thumbnail
            if "assets" in response:
                image_list = response["assets"]
                m_item['prod_img_url'] = []

                if image_list:
                    for image in image_list:
                        full_img_url = 'https:' + image["url"]
                        m_item['prod_img_url'].append(full_img_url.strip())
                else:
                    self.logger.error(f'No image here >>  {response.url}')

                m_item['prod_img_cnt'] = len(m_item['prod_img_url'])

            else:
                self.logger.error(f'No image here >>  {response.url}')

            # 최종 product_info 저장
            m_item['product_info'] = product_info

        except:
            m_item['product_info'] = product_info
            self.logger.error('Exception in parse-detail:: \n{:}'.format(traceback.format_exc()))

        yield m_item





