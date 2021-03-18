# -*- coding:utf-8 -*-
import datetime
from flask import request, g, jsonify, current_app
from ihome import db, redis_store
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from ihome.models import House, Order
from . import api


@api.route("/orders", methods=["POST"])
@login_required
def save_order():
    """保存订单"""
    user_id = g.user_id
    # 获取参数
    order_data = request.get_json()
    if not order_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    house_id = order_data.get("house_id")   # 预订的房屋编号
    start_date_str = order_data.get("start_date")   # 预订的起始时间
    end_date_str = order_data.get("end_date")   # 预订的结束时间

    # 参数检查
    if not all([house_id, start_date_str, end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 日期格式检查
    try:
        # 将请求的时间参数字符串转换为datetime类型
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        assert start_date <= end_date
        # 计算预订的天数
        days = (end_date - start_date).days + 1
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="日期格式错误")

    # 查询房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")


    # 预订的房屋是否是房东自己的
    if user_id == house.user_id:
        return jsonify(errno=RET.ROLEERR, errmsg="不能预订自己的房屋")

    # 确保用户预订的时间内，房屋没有被别人下单
    try:
        # 查询时间冲突订单数
        count = Order.query.filter(Order.house_id == house_id, Order.begin_date <= end_date,
                                   Order.end_date >= start_date).count()
        # select count(*) from order where
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="检查出错，请稍后重试")
    if count > 0:
        return jsonify(errno=RET.DATAERR, errmsg="房屋已被预订")

    # 订单总额
    amount = days * house.price

    # 保存订单数据
    order = Order(
        house_id=house_id,
        user_id=user_id,
        begin_date=start_date,
        end_date=end_date,
        days=days,
        house_price=house.price,
        amount=amount
    )

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存订单失败")
    return jsonify(errno=RET.OK, errmsg="OK", data={"order_id": order.id})


@api.route("/user/orders", methods=["GET"])
@login_required
def get_user_orders():
    """查询用户的订单信息"""
    user_id = g.user_id

    # 用户的身份，用户想要查询作为房客预订别人房子的订单，还是想要作为房东查询别人预订自己房子的订单
    role = request.args.get("role", "")

    # 查询订单数据
    try:
        if "landlord" == role:
            # 以房东的身份查询订单
            # 先查询属于自己的房子有哪些
            houses = House.query.filter(House.user_id == user_id).all()
            houses_ids = [house.id for house in houses]
            # 再查询预定了自己房子的订单
            orders = Order.query.filter(Order.user_id == user_id).order_by(Order.create_time.desc())
        else:
            # 以房客的身份查询订单，查询自己预订的订单
            orders = Order.query.filter(Order.user_id == user_id).order_by(Order.house_price.desc())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询订单信息失败")

    # 将订单对象转换为字典数据
    orders_dict_list = []
    if orders:
        for order in orders:
            orders_dict_list.append(order.to_dict())

    return jsonify(errno=RET.OK, errmsg="OK", data={"orders": orders_dict_list})


@api.route("/orders/<int:order_id>/status", methods=["POST"])
@login_required
def accept_reject_order(order_id):
    """接单，拒单"""
    user_id = g.user_id
    # 获取参数
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # action参数表明客户端请求的是接单还是拒单的行为
    action = req_data.get("action")
    if action not in ("accept", "reject"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
