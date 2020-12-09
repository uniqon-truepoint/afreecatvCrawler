# -*- coding: utf-8 -*-
from orator import DatabaseManager, Model
from orator.orm import belongs_to_many
from .settings import ORATOR_CONFIG
from .logger import logger as lg


db = DatabaseManager(ORATOR_CONFIG)
Model.set_connection_resolver(db)

class Afreecacreators(Model):
    """afreecaCreators 데이터 데이블"""
    __table__ = 'afreecacreators'

    @belongs_to_many
    def afreecachats(self):
        return Afreecachats

    # Live방송 중인 크리에이터 뽑아온다.
    def getLiveCreator(self):
        try:
            allRow = db.table(self.__table__).where('is_live', 1).get().all()
            rows = []
            for row in allRow:
                rows.append(row['creatorId'])
        except:
            rows = []
        return rows

    def updateLiveCreator(self, creatorIds, turnState):    
        for creatorId in creatorIds:
            if turnState == 'turn-off':
                row = db.table(self.__table__).where('creatorId', '=', creatorId).update(is_live=0)
                if row != 0:
                    lg.info(f'{creatorId}님이 라이브 방송을 종료했습니다')
            else:
                row = db.table(self.__table__).where('creatorId', '=', creatorId).update(is_live=1)
                if row != 0:
                    lg.info(f'{creatorId}님이 라이브 방송을 시작했습니다')
            
                
    def updateContent(self, creatorId, creatorName, startAt, resolution, videoQuality, endAt):
        db.table(self.__table__).where('creatorId', '=', creatorId).update(
            creatorName=creatorName,
            startAt=startAt,
            resolution=resolution,
            videoQuality=videoQuality,
            endAt=endAt
        )


class Afreecachats(Model):
    """afreecaChat 데이터 테이블"""
    __table__ = 'afreecachats'

    @belongs_to_many
    def afreecacreators(self):
        return Afreecacreators


class DatabasePipeline(object):
    """MySQL에 저장하기"""

    def __init__(self):
        """스크레이핑한 모든 item을 저장할 변수 선언"""
        self.items = []

    def process_item(self, item, spider):
        """각각의 아이템에 대한 처리 테이블에 INSERT"""
        afreecachat = Afreecachats()
        afreecachat.text = item['text']
        afreecachat.is_mobile = item['is_mobile']
        afreecachat.sex = item['sex']
        afreecachat.grade = item['grade']
        afreecachat.chattime = item['chattime']
        afreecachat.userId = item['userId']
        afreecachat.viewer = item['viewer']
        afreecachat.category = item['category']
        afreecachat.videoTitle = item['videoTitle']
        afreecachat.like = item['like']
        afreecachat.bookmark = item['bookmark']
        afreecachat.creatorId = item['creatorId']
        afreecachat.save()

        return item




