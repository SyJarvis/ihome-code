# -*- coding: UTF-8 -*-

from . import api
from flask import current_app, jsonify, make_response, request
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
from ihome import redis_store, constants
from ihome.libs.yuntongxun.sms import CCP
from ihome.models import User
import random

from ihome.tasks.task_sms import send_sms

@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证码
    :params image_code_id:  图片验证码编号
    :return: 正常：返回验证码图片，异常:json
    """
    # 业务逻辑处理
    # 生成验证码图片
    # 名字  真实文本   图片数据
    name, text, image_data = captcha.generate_captcha()
    # 将验证码真实值与编号保存到redis中
    try:
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES ,text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="save image code failed")
    # 返回图片
    # Content-Type: 'text/html'
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp

# # GET   /api/v1.0/sms_codes/<mobile>?image_code=xxxxximage_code_id=xxxx
# @api.route("/sms_codes/<re(r'1[134578]\d{9}'):mobile>",)
# def get_sms_code(mobile):
#     """获取短信验证码"""
#     # 获取参数
#     image_code = request.args.get("image_code")
#     image_code_id = request.args.get("image_code_id")
#
#     # 校验参数,mobile参数已经在正则表达式那里校验了，校验不成功也就不会进入函数内部
#     if not all([image_code, image_code_id]):
#         # 参数不完整
#         return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
#
#     # 业务逻辑处理
#     # 从redis中取出真实的图片验证码
#     try:
#         # 设置了过期时间，如果存储的数据过期了是以None的方式返回的，而不是返回数据
#         real_image_code = redis_store.get("image_code_%s"%image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
#     # 判断图片验证码是否过期
#     if real_image_code is None:
#         # 表示图片验证码没有或者过期
#         return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")
#     # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
#     try:
#         redis_store.delete("image_code_%s"%image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#
#     # 与用户填写的进行对比校验
#     if real_image_code.decode().lower() != image_code.lower():
#         # 表示用户填写错误
#         return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
#
#     # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
#     try:
#         send_flag = redis_store.get("send_sms_code_%s"%mobile)
#     except Exception as e:
#         current_app.logger.error(e)
#     else:
#         if send_flag is not None:
#             # 表示在60秒内之前有过发送的记录
#             return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请６０秒后重试")
#
#
#
#     # 判断手机号是否存在,单条记录不存在返回None
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except Exception as e:
#         current_app.logger.error(e)
#     else:
#         if user is not None:
#             # 表示手机号已存在
#             return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
#
#     # 如果手机号不存在，则生成短信验证码
#     sms_code = "%06d" % random.randint(0, 999999)
#
#     # 保存真实的短信验证码
#     try:
#         redis_store.setex("sms_code_%s"%mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
#         # 保存发送给这个手机号的记录，防止用户在60s秒内再次发出发送短信的操作
#         redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")
#
#     # 发送短信
#     try:
#         ccp = CCP()
#         result = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
#
#     # 返回值
#     if result == 0:
#         # 发送成功
#         return jsonify(errno=RET.OK, errmsg="发送成功")
#     else:
#         return jsonify(errno=RET.THIRDERR, errmsg="发送失败")



# GET   /api/v1.0/sms_codes/<mobile>?image_code=xxxxximage_code_id=xxxx
@api.route("/sms_codes/<re(r'1[134578]\d{9}'):mobile>",)
def get_sms_code(mobile):
    """获取短信验证码"""
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    # 校验参数,mobile参数已经在正则表达式那里校验了，校验不成功也就不会进入函数内部
    if not all([image_code, image_code_id]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        # 设置了过期时间，如果存储的数据过期了是以None的方式返回的，而不是返回数据
        real_image_code = redis_store.get("image_code_%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
    # 判断图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码没有或者过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")
    # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 与用户填写的进行对比校验
    if real_image_code.decode().lower() != image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s"%mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            # 表示在60秒内之前有过发送的记录
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请６０秒后重试")



    # 判断手机号是否存在,单条记录不存在返回None
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在，则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)

    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s"%mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录，防止用户在60s秒内再次发出发送短信的操作
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # 发送短信
    # 使用celery发送异步短信,delay调用后立即返回
    send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)

    # 返回值
    # 发送成功
    return jsonify(errno=RET.OK, errmsg="发送成功")



