import os

class Config:
    UPLOAD_FOLDER = r'C:\Users\relic\Documents\School\Engineering_Cam\Part IIB\Masters Project\sam\segment-anything\backend\temp'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_MAPS_STATIC_API_KEY = os.getenv('GOOGLE_MAPS_STATIC_API_KEY')
    MODEL_CHECKPOINT_PATH = r"C:\Users\relic\Documents\School\Engineering_Cam\Part IIB\Masters Project\sam\segment-anything\backend\sam_vit_h_4b8939.pth"
    MODEL_TYPE = "vit_h"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True