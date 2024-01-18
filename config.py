import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    #DEV_DATABASE_URL = os.getenv('DEV_DATABASE_URL')

    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = os.getenv('DATABASE_PORT')

    # ADMIN ACCOUNT
    #DATABASE_USER_A = os.getenv('DATABASE_USER_A')
    #DATABASE_PASSWORD_A = os.getenv('DATABASE_PASSWORD_A')

    #USER ACCOUNT
    #DATABASE_USER_U = os.getenv('DATABASE_USER_U')
    #DATABASE_PASSWORD_U = os.getenv('DATABASE_PASSWORD_U')

