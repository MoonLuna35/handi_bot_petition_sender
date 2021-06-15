import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv


def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class _Const(object):
    def __init__(self):
        load_dotenv(find_dotenv())

    @constant
    def DB_NAME():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_DB_NAME")
        else:
            return os.getenv("PROD_DB_NAME")
    @constant
    def DB_PWD():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_DB_PWD")
        else:
            return os.getenv("PROD_DB_PWD")
    @constant
    def DB_HOST():
        return os.getenv("DB_HOST")
    @constant
    def DB_DATA_BASE():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_DB_DATA_BASE")
        else:
            return os.getenv("PROD_DB_DATA_BASE")
    @constant
    def IMG_PATH():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_IMG_PATH")
        else:
            return os.getenv("PROD_IMG_PATH")
    @constant
    def LOG_PATH():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_LOG_PATH")
        else:
            return os.getenv("PROD_LOG_PATH")
    @constant
    def MAIL_STMP_SERVER():
        return os.getenv("MAIL_STMP_SERVER")
    @constant
    def MAIL_STMP_PORT():
        return os.getenv("MAIL_STMP_PORT")
    @constant
    def MAIL_ADRESS_FROM():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_MAIL_ADRESS_FROM")
        else:
            return os.getenv("PROD_MAIL_ADRESS_FROM")
    @constant
    def MAIL_ADRESS_FROM_PWD():
        return os.getenv("MAIL_ADRESS_FROM_PWD")
    @constant
    def MAIL_ADRESS_TO():
        return os.getenv("MAIL_ADRESS_TO")
    @constant
    def MAIL_ADRESS_FROM_NAME():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_MAIL_ADRESS_FROM_NAME")
        else:
            return os.getenv("PROD_MAIL_ADRESS_FROM_NAME")
    @constant
    def TWITTER_CONSUMER():
        return os.getenv("TWITTER_CONSUMER")
    @constant
    def TWITTER_CONSUMER_SECRET():
        return os.getenv("TWITTER_CONSUMER_SECRET")
    @constant
    def TWITTER_ACESS_TOKEN():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_TWITTER_ACESS_TOKEN")
        else:
            return os.getenv("PROD_TWITTER_ACESS_TOKEN")
    @constant
    def TWITTER_ACESS_TOKEN_SECRET():
        if dirname(__file__).find("dev") != -1:
            return os.getenv("DEV_TWITTER_ACESS_TOKEN_SECRET")
        else:
            return os.getenv("PROD_TWITTER_ACESS_TOKEN_SECRET")

