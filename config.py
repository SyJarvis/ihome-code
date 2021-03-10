# -*- coding:utf-8 -*-
import redis


class Config(object):
    """配置信息"""

    SECRET_KEY = "qwertyuiopasdfghjkl123456789"

    # 数据库
    # "mysql://root:mysql0220@127.0.0.1:3306/ihome?charset=utf8mb4"
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql0220@127.0.0.1:3306/ihome?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 对cookie中的session_id进行隐藏，混淆处理
    SESSION_USE_SIGNER = True
    # session数据的有效期，单位秒
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境的配置信息"""
    pass

config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}




