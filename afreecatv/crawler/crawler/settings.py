from .configController import ConfigController

config = ConfigController()
config.load()

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.SeleniumMiddleware': 100
}

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 32
CONCURRENT_REQUESTS_PER_IP = 32
ITEM_PIPELINES = {
   'crawler.pipelines.DatabasePipeline': 300,
}

ORATOR_CONFIG = {    
    'mysql': {
        'driver': config.DB_DRIVER,
        'host': config.DB_HOST,
        'database': config.DB_NAME,
        'user': config.DB_USER,
        'password': config.DB_PASSWORD,
        'port': config.DB_PORT
    }
}