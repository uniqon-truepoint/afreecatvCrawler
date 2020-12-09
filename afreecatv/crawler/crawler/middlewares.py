from scrapy import signals
from .logger import logger as lg
from time import sleep
from datetime import datetime as dt
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from .pipelines import Afreecacreators
import requests, re
from .configController import ConfigController
import os, subprocess

chatAllData = []

class SeleniumMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(
            middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(
            middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        self.config = ConfigController()
        self.config.load()
        CHROMEDRIVER_PATH = r'C:\Users\WHILETRUESECOND\Desktop\tp-mvp\collectors\afreecatv\crawler\crawler\drivers\chromedriver.exe'
        WINDOW_SIZE = "1920, 1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 크롬창이 열리지 않게
        chrome_options.add_argument("--no-sandbox") # GUI를 사용할 수 없는 환경에서 설정, Linux, dorker 등...
        chrome_options.add_argument("--disable-gpu") # GUI를 사용할 수 없는 환경에서 설정, Linux, dorker 등...
        chrome_options.add_argument(f"--window-size={ WINDOW_SIZE }")
        chrome_options.add_argument("--mute-audio") # 브라우저 음소거
        # selenium 성능 향상을 위한 옵션 제어
        prefs = {'profile.default_content_setting_values': 
        {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2,
        'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2,
        'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2,
        'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 
        'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2,
        'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
        chrome_options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options )
        self.driver.get("https://login.afreecatv.com/afreeca/login.php?szFrom=full&request_uri=http%3A%2F%2Fafreecatv.com%2F")
        sleep(3)
        elem_login = self.driver.find_element_by_id("uid")
        elem_login.clear()
        elem_login.send_keys(self.config.AFREECA_ID) 
        elem_login = self.driver.find_element_by_id("password")
        elem_login.clear()
        elem_login.send_keys(self.config.AFREECA_PASSWORD, Keys.ENTER)
        lg.info('크롬브라우저로 아프리카 로그인')
        sleep(3)


    def process_request( self, request, spider ):
        self.driver.get( request.url )
        sleep(3)
        self.driver.find_element_by_xpath('//*[@id="stop_screen"]/dl/dd[2]/a').click()
        self.creatorId  = request.url[26:-1]

        # 채팅창 제어 변수 초깃값
        chatNum = 1
        liveEndPoint = 0 # 생방송 상대 여부 판별
        tryTime = 0 # 채팅 업로드 시도횟수
        
        def liveEndCheck(self, chatNum, tryTime, liveEndPoint):
            response = requests.get(request.url)
            title  = re.search('"twitter:title" content=".*"', response.text, re.I)
            getTitle = title.group()[-12:-2]
            try:
                next_chating_present = EC.presence_of_element_located((By.ID, f'{chatNum+1}'))
                WebDriverWait(self.driver, 10, poll_frequency=0.5).until(next_chating_present)
            except:
                if getTitle == '방송중이지 않습니다':
                    lg.info(f'{self.creatorId} 방송 종료')
                    liveEndPoint = liveEndPoint + 1
                    return liveEndPoint
                elif self.driver.find_element_by_xpath('//*[@id="afreecatv_player"]/div[12]/div/div/div[8]').get_attribute("style") == '':
                    lg.warning(f'{self.creatorId} 블라인드 처리')
                    liveEndPoint = liveEndPoint + 1
                    return liveEndPoint
                elif self.driver.find_element_by_xpath('//*[@id="afreecatv_player"]/div[12]/div/div/div[3]').get_attribute("style") == '':
                    lg.warning(f'{self.creatorId} 19세 방송중')
                    try:
                        self.driver.find_element_by_xpath('//*[@id="afreecatv_player"]/div[12]/div/div/div[3]/div/button[1]').click()
                    except:
                        pass
                    tryTime = tryTime + 1

                    if tryTime == 13:
                        lg.warning(f'{self.creatorId}님의 19세 방송중 상태 불안정에 따른 새로고침을 실시: 2분 채팅대기')
                        self.driver.refresh()
                        sleep(2)
                        try:
                            self.driver.find_element_by_xpath('//*[@id="stop_screen"]/dl/dd[2]/a').click()
                        except:
                            pass
                        chatNum = 1
                        tryTime = 0
                    
                    liveEndCheck(self, chatNum, tryTime, liveEndPoint)
                    
                elif self.driver.find_element_by_xpath('//*[@id="afreecatv_player"]/div[12]/div/div/div[7]').get_attribute("style") == '':
                    lg.warning(f'{self.creatorId} 비밀번호 설정')
                    liveEndPoint = liveEndPoint + 1
                    return liveEndPoint 
                else:
                    tryTime = tryTime + 1

                    if tryTime == 13:
                        lg.warning(f'{self.creatorId}님의 방송 상태 불안정에 따른 새로고침을 실시: 2분 채팅대기')
                        self.driver.refresh()
                        sleep(2)
                        try:
                            self.driver.find_element_by_xpath('//*[@id="stop_screen"]/dl/dd[2]/a').click()
                        except:
                            pass
                        chatNum = 1
                        tryTime = 0
                    
                    liveEndCheck(self, chatNum, tryTime, liveEndPoint)

        while True:
            if liveEndCheck(self, chatNum, tryTime, liveEndPoint) == 1:
                break
            chatEachData = {}
            atTime = dt.now().strftime('%Y-%m-%d %H:%M:%S')
            chatIdNum = f'//*[@id=\"{chatNum}\"]'
            user = f'//*[@id=\"{chatNum}\"]/preceding-sibling::dt'
            userId = f'//*[@id=\"{chatNum}\"]/preceding-sibling::dt/a'
            
            try:
                chatEachData['userId'] = self.driver.find_element_by_xpath(userId).get_attribute("user_id")
                chatEachData['is_mobile'] = self.driver.find_element_by_xpath(userId).get_attribute("is_mobile")
                chatEachData['category'] = self.driver.find_element_by_xpath('//*[@id="player_area"]/div[2]/div[2]/ul/li[4]/span').text
                chatEachData['videoTitle'] = self.driver.find_element_by_xpath('//*[@id="player_area"]/div[2]/div[2]/div[4]/span').text
                chatEachData['like'] = self.driver.find_element_by_xpath('//*[@id="player_area"]/div[2]/div[2]/div[6]/ul/li[1]/span').text
                chatEachData['bookmark'] = self.driver.find_element_by_xpath('//*[@id="player_area"]/div[2]/div[2]/div[6]/ul/li[2]/span').text
                chatEachData['viewer'] = self.driver.find_element_by_xpath('//*[@id="nAllViewer"]').text
                chatEachData['grade'] = self.driver.find_element_by_xpath(user).get_attribute("class").split('_')[0]
                chatEachData['sex'] = self.driver.find_element_by_xpath(user).get_attribute("class").split('_')[1]
                chatEachData['text'] = self.driver.find_element_by_xpath(chatIdNum).text
                chatEachData['creatorId'] = self.creatorId
                chatEachData['chattime'] = atTime
                chatAllData.append(chatEachData)
            except:           
                lg.warning(f'{self.creatorId}님 방송의 채팅량이 많아 다시 주기를 갱신')
                self.driver.refresh()
                sleep(2)
                try:
                    self.driver.find_element_by_xpath('//*[@id="stop_screen"]/dl/dd[2]/a').click()
                except:
                    pass
                chatNum = 1
                    
            chatNum = chatNum + 1
            
        body = to_bytes( text=self.driver.page_source )
        return HtmlResponse( url=request.url, body=body, encoding='utf-8', request=request )
    
    def spider_closed(self, spider):
        lg.info(f'{self.creatorId} 타겟방송 크롬브라우저 종료 및 프로세스 킬')
        afreecaCreator = Afreecacreators()
        afreecaCreator.updateLiveCreator([self.creatorId],'turn-off')
        self.driver.close()
        self.driver.quit()



