# backend/config.py

class Config:
    SECRET_KEY = '123456'  # 替换为强密码
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://game_user:123456@47.103.42.195/tiandaoqiyuan'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '123456'  # 替换为强密码
    JWT_ACCESS_TOKEN_EXPIRES = False
