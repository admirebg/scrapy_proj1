# ==========================================================================
# 신규 브랜드 크롤링
# ==========================================================================
import os
from datetime import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from shopper.middleware.slack_middleware import SlackSum
from shopper.spiders.chanel import ChanelSpider
from shopper.spiders.louisvuitton import LouisVuittonSpider
# from shopper.spiders.prada import PradaSpider
from shopper.spiders.ysl import YslSpider
from shopper.spiders.gucci import GucciSpider
from shopper.spiders.hermes import HermesSpider

settings = get_project_settings()

# 로그 폴더 생성
log_dir = './log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# 로그 파일 생성
today = datetime.now()
log_file_name = "[%04d%02d%02d_%02d%02d%02d]new_brand_log.txt" %\
                (today.year, today.month, today.day, today.hour, today.minute, today.second)
# settings.set('LOG_FILE', log_dir + "/" + log_file_name)

file_created = "%04d%02d%02d_%02d%02d%02d" % \
               (today.year, today.month, today.day, today.hour, today.minute, today.second)
log_full_path = settings['LOG_DIR'] + f"/{file_created}.log"
settings.set('LOG_FILE', log_full_path)

# 로그 레벨 설정
settings.set('LOG_LEVEL', 'DEBUG')
# settings.set('LOG_LEVEL', 'INFO')
# settings.set('LOG_LEVEL', 'ERROR')

# pipeline 설정
settings.setdict({'ITEM_PIPELINES': {
    # 'shopper.pipelines.CsvPipeline': 300,  # 크롤링결과를 csv 파일로 export
    'shopper.pipelines.JsonPipeline': 300,  # 크롤링결과를 json 파일로 export
    # 'shopper.pipelines.CrawlNewPipeline': 300, # DB Import
}})
# 슬랙 연동
settings.setdict({'EXTENSIONS': {
    'shopper.middleware.slack_middleware.SlackStats': 100,
}})
slack = SlackSum(settings.get("SLACK_TOKEN"), settings.get("SLACK_CHANNEL"), settings.get("SLACK_BOT"))

process = CrawlerProcess(settings)

# process.crawl(ChanelSpider)
# process.crawl(YslSpider)
# process.crawl(LouisVuittonSpider)
# process.crawl(GucciSpider)
process.crawl(HermesSpider)

process.start()
process.join()

# 크롤링 결과 데이터 보내는
# slack.total_finish()