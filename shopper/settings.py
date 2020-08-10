# -*- coding: utf-8 -*-

# Scrapy settings for shopper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import os

BOT_NAME = 'shopper'

SPIDER_MODULES = ['shopper.spiders']
NEWSPIDER_MODULE = 'shopper.spiders'

# RETRY_TIMES = 2
# RETRY_HTTP_CODES = [403]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'


# USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
# USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Connection': 'keep-alive'
  # 'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'shopper.middlewares.ShopperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'shopper.middlewares.ShopperDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'shopper.pipelines.ShopperPipeline': 300,
   #  'shopper.pipelines.JsonPipeline': 300,
   #  'shopper.pipelines.MysqlPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# 도메인 내에서 스파이더 요청 간격 조정옵션
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 6.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DNS_TIMEOUT = 15

# 로그 레벨 설정
# LOG_LEVEL = 'INFO'
LOG_LEVEL = 'ERROR'
# LOG_LEVEL = 'DEBUG'

LOG_DIR = './log'
# LOG_FILE = 'log.txt'

SLACK_TOKEN = "xoxb-705881037367-1179053414993-vgb2Qkqs23Z77XBCuft1MjiP"
# crawling : 크롤링 결과 전달받는 채널
SLACK_CHANNEL = ["상품_크롤링_알림"]
SLACK_BOT = "crawler_test"

# s3 버킷 및 cloudfront 사용하도록 사용 설정
AWS_STORAGE_BUCKET_NAME = 'secondhands-product'
AWS_DOMAIN_NAME = f'{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = f"https://{AWS_DOMAIN_NAME}"


# 로컬 내 계정 정보 secret 파일 호출
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
secret_file = os.path.join(BASE_DIR, '../secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        if setting in secrets:
            return secrets[setting]
        else:
            return ""
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        print(f"ERROR WHILE SECRET : {error_msg}")
        return 


S3_ACCESS_KEY_ID = get_secret("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = get_secret("S3_SECRET_ACCESS_KEY")
RDS_ACCESS_KEY_ID = get_secret("RDS_ACCESS_KEY_ID")
RDS_SECRET_ACCESS_KEY = get_secret("RDS_SECRET_ACCESS_KEY")

IS_LOCAL = get_secret("IS_LOCAL")
IS_CRAWL_TEST = get_secret("IS_CRAWL_TEST")
if IS_LOCAL == "True":
    MYSQL_PASSWORD = get_secret("DB_PASSWORD")
else:
    MYSQL_PASSWORD = ""

if IS_CRAWL_TEST == "True":
    MYSQL_HOST = get_secret("DB_HOST_LOCAL")
    MYSQL_PORT = get_secret("DB_PORT_LOCAL")
    MYSQL_USER = get_secret("DB_USERNAME_LOCAL")
    MYSQL_DB = get_secret("DB_NAME_LOCAL")

else:
    MYSQL_HOST = get_secret("DB_HOST")
    MYSQL_PORT = get_secret("DB_PORT")
    MYSQL_USER = get_secret("DB_USERNAME")
    MYSQL_DB = get_secret("DB_NAME")
