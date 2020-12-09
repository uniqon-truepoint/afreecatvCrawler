import os
from dotenv import load_dotenv

class ConfigController:
    environmnet = ''

    def __init__(self):
        # dirpath = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(dotenv_path=r"C:\Users\WHILETRUESECOND\Desktop\tp-mvp\collectors\afreecatv\crawler\crawler\.env", verbose=True)
        

    def load(self):
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_PORT = int(os.getenv('DB_PORT'))
        self.AFREECA_ID = os.getenv('AFREECA_ID')
        self.AFREECA_PASSWORD = os.getenv('AFREECA_PASSWORD')
        self.DB_DRIVER = os.getenv('DB_DRIVER')