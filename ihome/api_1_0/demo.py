# -*- coding: utf-8 -*-
from . import api
from ihome import db, models
from flask import current_app


@api.route('/index')
def index():
    # logging.logger.error("err msg")  # 错误级别
    # logging.logger.warn("")  # 警告级别
    # logging.logger.info("")  # 消息提示级别
    # logging.logger.debug("")  # 调试级别
    return "index page"