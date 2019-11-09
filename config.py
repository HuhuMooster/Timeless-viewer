import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'PCY"Tl$#kj=i9D%kPozpi9:G5'
    MONGO_URI = 'mongodb://localhost:27017/timeless'
