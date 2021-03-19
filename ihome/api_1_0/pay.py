# coding:utf-8

from . import api
from flask import jsonify, current_app, g, request
from ihome.utils.commons import login_required
from ihome.models import Order
from ihome.utils.response_code import RET
from alipay import AliPay
from ihome import constants, db
import os


@api.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
    """发起支付宝支付"""
    user_id = g.user_id

    # 判断订单状态
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id, Order.status == "WAIT_PAYMENT").first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if order is None:
        return jsonify(errno=RET.NODATA, errmsg="订单数据有误")


    # 创建支付宝sdk的工具对像
    alipay_client = AliPay(
        appid="2016101500689753",
        app_notify_url=None,        # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),    # 私钥
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),   #　支付宝公钥
        sign_type="RSA2",
        debug = True
    )

    print(os.path.dirname(__file__))

    # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    # 沙箱环境 https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order.id,    # 订单编号
        total_amount=str(order.amount/100.0),    # 总金额
        subject=u"爱家租房 %s" % order_id,         # 订单标题
        return_url="http://192.168.0.103:5000/payComplete.html",
        notify_url=None
    )

    # 构建让用户跳转的支付链接地址
    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})



@api.route("/order/payment", methods=["PUT"])
def save_order_payment_result():
    """保存订单支付结果"""

    alipay_dict = request.form.to_dict()

    # 对支付宝的数据进行分离，提取出支付宝的签名参数sign，和剩下的其他数据
    alipay_sign = alipay_dict.pop("sign")

    # 创建支付宝sdk的工具对象
    alipay_client = AliPay(
        appid="2016101500689753",
        app_notify_url=None,        # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),    # 私钥
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),   #　支付宝公钥
        sign_type="RSA2",
        debug = True
    )

    # 借助工具验证参数的合法性
    # 如果确定参数是支付宝的返回True，否则返回False
    result = alipay_client.verify(alipay_dict, alipay_sign)
    if result:
        # 修改数据库的订单状态
        order_id = alipay_dict.get("out_trade_no")
        trade_no = alipay_dict.get("trade_no")  # 支付宝的交易号
        print(trade_no)
        try:
            Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
            db.session.commit()
        except Exception as e:
            print("error")
            current_app.logger.error(e)
            db.session.rollback()

    return jsonify(errno=RET.OK, errmsg="OK")

#





