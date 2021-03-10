循环导包的问题，

把一个包延迟导入。

一个工程目录大概就是下面这个样子

```
ihome
	ihome
		api_1_0
			__init__.py
			views.py
		libs
		static
		utils
		__init__.py
		models.py
	config.py
	manage.pu
```

config.py

```
放置配置参数
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
    REDIS_HOST = '122.51.52.108'
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
```

manage.py

```
# 启动文件
# -*- coding:utf-8 -*-

from ihome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
app = create_app('develop')

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    app.run()
```

ihome.\_\_init\_\_.py

```
# -*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config_map
from flask_session import Session
from flask_wtf import CSRFProtect
import redis
import pymysql
pymysql.install_as_MySQLdb()

# 数据库
db = SQLAlchemy()
# 创建redis连接对象
redis_store = None
# 为flask补充csrf防护机制
csrf = CSRFProtect()

# 设置日志的记录等级
logging.basicConfig(level=logging.WARNING)
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handle = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志的记录格式
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录设置日志记录格式
file_log_handle.setFormatter(formatter)
# 为全局的日志工具对象(flask app使用的)添加日志记录器
logging.getLogger().addHandler(file_log_handle)

# 工厂模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str 配置模式的模式名，("develop", "product")
    :return:
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)
    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask_session,将Session数据保存到redis中
    Session(app)
    # CSRF认证
    csrf.init_app(app)

    # 注册蓝图
    from ihome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    return app
```



