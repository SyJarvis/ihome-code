# -*- coding:utf-8 -*-
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from ihome import constants

class BaseModel(object):
    """模型基类， 为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "ih_user_profile"
    id = db.Column(db.Integer, primary_key=True)    # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)    # 用户昵称unique唯一性，nullable不为空，默认可以为空
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号码
    real_name = db.Column(db.String(32))    # 真实姓名
    id_card = db.Column(db.String(20))  # 身份证号
    avatar_url = db.Column(db.String(128))  # 用户头像路径
    houses = db.relationship("House", backref="user")
    orders = db.relationship("Order", backref="user")

    # 加上property装饰器后，会把函数变为属性，属性名即为函数名
    @property
    def password(self):
        """读取属性的函数行为"""
        # 函数的返回值会作为属性值传递
        # print(user.password)  # 读取属性时被调用
        # return "xxxx"
        raise AttributeError("这个属性只能设置，不能读取")
    # 使用这个装饰器，设置属性
    @password.setter
    def password(self, value):
        """
        设置属性    user.password = "xxxxxx"
        :param value: 设置属性时的数据  value="xxxxxx",原始的明文密码
        :return:
        """
        self.password_hash = generate_password_hash(value)

    def check_password(self, passwd):
        """
        校验密码的正确性
        :param passwd: 用户登录时填写的原始密码
        :return: 如果正确返回true，否则返回false
        """
        return check_password_hash(self.password_hash, passwd)

    # def generate_password_hash(self, origin_password):
    #     """ 对密码进行加密"""
    #     self.password_hash = generate_password_hash(origin_password)

    def to_dict(self):
        """
        将数据转换成字典
        :return: 字典
        """
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "mobile": self.mobile,
            "avatar": constants.QINIU_URL_DOMAIN + self.avatar_url if self.avatar_url else "",
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:S")
        }

        return user_dict

    def auto_to_dict(self):
        """
        将实名信息转换成字典
        :return: 字典
        """
        auto_dict = {
            "user_id": self.id,
            "real_name": self.real_name,
            "id_card": self.id_card
        }
        return auto_dict


class Area(BaseModel, db.Model):
    """城区"""

    __tablename__ = "ih_area_info"

    id = db.Column(db.Integer, primary_key=True)    # 区域编号
    name = db.Column(db.String(32), nullable=False) # 区域名字
    houses = db.relationship("House", backref='area')  # 区域的房屋


    def to_dict(self):
        """将对象转换为字典"""
        area_dict = {
            "aid": self.id,
            "aname": self.name
        }

        return area_dict



house_facility = db.Table(
    "ih_house_facility",
    db.Column("house_id", db.Integer, db.ForeignKey("ih_house_info.id"), primary_key=True),
    db.Column("facility_id", db.Integer, db.ForeignKey("ih_facility_info.id"), primary_key=True)    #

)

class Order(BaseModel, db.Model):
    """订单"""

    __tablename__ = "ih_order_info"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)
    begin_date = db.Column(db.DateTime, nullable=False) # 预定的起始时间
    end_date = db.Column(db.DateTime, nullable=False)   # 预定的结束时间
    days = db.Column(db.Integer, nullable=False)    # 预定的总天数
    house_price = db.Column(db.Integer, nullable=False) # 房屋的单价
    amount = db.Column(db.Integer, nullable=False)  # 房屋的单价
    status = db.Column(
        db.Enum(
            "WAIT_ACCEPT",  # 待接单
            "WAIT_PAYMENT", # 待支付
            "PAID",     # 已支付
            "WAIT_COMMENT",     # 待评价
            "COMPLETE",     # 已完成
            "CANCELED",     # 已取消
            "REJECTED", # 已拒单
        ),
        default="WAIT_ACCEPT", index=True)
    comment = db.Column(db.Text)    # 订单的评论信息或者拒单原因
    trade_no = db.Column(db.String(80))     # 交易的流水号，支付宝的




class House(BaseModel, db.Model):
    """房屋信息"""

    __tablename__ = "ih_house_info"

    id = db.Column(db.Integer, primary_key=True)    # 房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("ih_area_info.id"), nullable=False)
    title = db.Column(db.String(64), nullable=False)    # 标题
    price = db.Column(db.Integer, default=0)
    address = db.Column(db.String(512), default="") # 地址
    room_count = db.Column(db.Integer, default=1)
    acreage = db.Column(db.Integer, default=0)  # 房屋面积
    unit = db.Column(db.String(32), default="") # 房屋单元， 如几室几厅
    capacity = db.Column(db.Integer, default=1) # 房屋容纳的人数
    beds = db.Column(db.String(64), default="") # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0)  # 房屋押金
    min_days = db.Column(db.Integer, default=1) # 最少入住天数
    max_days = db.Column(db.Integer, default=0) # 最多入住天数，0表示不限制
    order_count = db.Column(db.Integer, default=0)  # 预定完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default="")
    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋的设施
    images = db.relationship("HouseImage")  # 房屋的图片
    orders = db.relationship("Order", backref="house")  # 房屋的订单


class Facility(BaseModel, db.Model):
    """设施信息"""

    __tablename__ = "ih_facility_info"

    id = db.Column(db.Integer, primary_key=True)    # 设施编号
    name = db.Column(db.String(32), nullable=False) # 设施名字

class HouseImage(BaseModel, db.Model):
    """房屋图片"""

    __tablename__ = "ih_house_image"

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)
    url = db.Column(db.String(256), nullable=False)