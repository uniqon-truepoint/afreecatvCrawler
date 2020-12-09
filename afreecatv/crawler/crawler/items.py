import scrapy


class AfreecatvChat(scrapy.Item):
    viewer = scrapy.Field()
    category = scrapy.Field()
    videoTitle = scrapy.Field()
    text = scrapy.Field()
    is_mobile = scrapy.Field()
    sex = scrapy.Field()
    grade = scrapy.Field()
    chattime = scrapy.Field()
    userId = scrapy.Field()
    like = scrapy.Field()
    bookmark = scrapy.Field()
    creatorId = scrapy.Field()

class AfreecatvCreators(scrapy.Item):
    creatorName = scrapy.Field()
    startAt = scrapy.Field()
    resolution = scrapy.Field()
    videoQuality = scrapy.Field()
    endAt = scrapy.Field()