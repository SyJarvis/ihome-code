logging的使用

```
import logging
from logging.handlers import RotatingFileHandler


# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handle = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志的记录格式
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录设置日志记录格式
file_log_handle.setFormatter(formatter)
```

```
logging记录日志信息的用法

logging.logger.error("err msg")	# 错误级别
logging.logger.warn("")		# 警告级别
logging.logger.info("")		# 消息提示级别
logging.logger.debug("")	# 调试级别
flask里的current_app这个全局对象包含了logging这个包的实例对象，所以可以直接调用
from flask import current_app
current_app.logger.error("err msg")
```

