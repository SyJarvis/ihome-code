from . import api
from flask import request, jsonify, current_app, session
from ihome.utils.response_code import RET
import re
from ihome import redis_store, db
from ihome.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from ihome import constants

@api.route("/users", methods=['POST'])
def register():
    """注册
    请求的参数：手机号、短信验证码、密码、确认密码
    参数格式:json
    """
    # 获取请求的json数据，返回字典
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("passwd")
    password2 = req_dict.get("passwd2")

    # 校验参数
    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 判断手机号格式
    if not re.match(r"1[34578]\d{9}", mobile):
        # 不匹配，表示格式不对
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')

    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg='两次密码不一致')

    # 业务逻辑处理
    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s"%mobile)
        print(real_sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码失效")

    # 删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    real_sms_code = real_sms_code.decode()
    # real_sms_code = str(real_sms_code, encoding='utf-8')
    # 判断用户填写短信验证码的正确性
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")
    # 判断用户的手机号是否注册过
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    # else:
    #     if user is not None:
    #         # 表示手机号已存在
    #         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 保存用户的注册数据到数据库中
    # 减少数据库的查询，尽量把查询和插入放到一起，如此可以减少对数据库的操作，能够减少一次是一次。
    # 插入一条数据，会去校验数据的唯一性，因为mobile键设置了唯一性unique,唯一约束
    user = User(name=mobile, mobile=mobile)
    # user.generate_password_hash(password)
    user.password = password    # 设置属性
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚，回滚到上一次commit()操作之前的状态
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST,errmsg="手机号已存在")
    except Exception as e:
        # 数据库事务的回滚
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')

    # 保存登录状态到session中
    session['name'] = mobile
    session['mobile'] = mobile
    session['user_id'] = user.id
    # 返回结果
    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route('/sessions', methods=['POST'])
def login():
    """
    用户登录
    参数“手机号码、密码
    :return:
    """

    # 获取参数
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')
    # 校验参数
    # 参数完整的校验
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 手机号的格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')
    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录：”access_nums_请求的ip"
    user_ip = request.remote_addr   # 用户的ip地址
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
        print('access_nums', access_nums)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg='错误次数过多，请稍后重试')
    # 从数据库中根据手机号查询用户的数据对象，判断是否有此用户
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户信息失败')
    # 用数据库的密码与用户填写的密码进行对比验证
    print('check_password', user.check_password(password))
    print('user', user)
    if user is None or not user.check_password(password):
        # 如果验证失败，记录错误次数，返回信息
        try:
            redis_store.incr("access_num_%s"%user_ip)
            redis_store.expire("access_num_%s"%user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR, errmsg='用户名或密码错误')


    # 如果验证相同，保存登录状态session
    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id
    return jsonify(errno=RET.OK, errmsg="登录成功")


@api.route("/session", methods=['GET'])
def check_login():
    """
    检查登录状态
    :return:
    """
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name":name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")




