# 数据库扩展包flask-sqlalchemy



## 1.使用sqlalchemy的配置





### 使用Flask-SQLAlchemy管理数据库

使用Flask-SQLAlchemy扩展操作数据库，首先需要建立数据库连接。数据库连接通过URl指定，而且程序使用的数据库必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URL键中。



对比Django和Flask中的数据库设置：





flask数据库配置

```
# 设置连接数据库的URL
app.config["SQLALCHEMY_DATABASE_URL"] = "mysql+mysqlconnector://root:mysql0220@127.0.0.1:3306/test1?charset=utf8mb4"

# 设置每次请求结束后会自动提交数据库中的改动
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
```





表名命名的规范

ihome ->

tb_user

### 02创建模型类

```
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(appfro)

class Role(db.Model):
    """用户角色/身份表"""
    __tablename__ = "tbl_roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        """定义之后，可以让现实对象的时候更直观"""
        return "Role object: name=%s" % self.name

class User(db.Model):
    __tablename__ = "tbl_users" # 指明表名

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id"))

    def __repr__(self):
        return "User objects name=%s" % self.name
```



### 03创建数据库表

```

if __name__ == '__main__':
	# 清除数据库里的所有表
    db.drop_all()

    # 创建所有的表
    db.create_all()
```



### 04保存数据

```


# 创建对象
role1 = Role(name="admin")
# session记录对象任务
db.session.add(role1)
# 提交
db.session.commit()

role2 = Role(name="stuff")
db.session.add(role2)
db.session.commit()

us1 = User(name="wang", email="wang@163.com", password="123456", role_id=role1.id)
us2 = User(name="zhang", email="zhang@189.com", password="201512", role_id=role2.id)
us3 = User(name="chen", email="chen@163.com", password="987654", role_id=role2.id)
us4 = User(name="zhou", email="zhou@163.com", password="456789", role_id=role1.id)
db.session.add_all([us1, us2, us3, us4])
db.session.commit()
```



### 05sqlalchemy数据查询

```
query = query.filter(User.status == int(req.get('status')))
list = query.order_by(User.uid.desc()).all()[offset:limit]
```



### 06关联查询与自定义显示信息

```
User绑定外键Role，Role有个属性反关联到user，所有绑定到role的user对象都会在一个列表里。
from db_demo import Role, User

ro = Role.query.get(1)
type(ro)
ro.users	# 返回的是列表对象，外键

user = User.query.get(1)
user.role_id

Role.query.get(user.role_id)

user.role
user.role.name

# 改变对象的显示信息object
def __repr__(self):
	return "User objects name=%s" % self.name
```



### 07数据的修改与删除

##### 修改

```
from db_demo import User
from db_demo import db

# 第一种方法
user = User.query.get(1)
user.name
user.name = 'itcast'
db.session.add(user)
db.session.commit()

# 第二种方法
User.query.filter_by(name='zhou').update({'name': 'python', 'email': 'python@itast,cn'})
db.session.commit()

```

##### 删除

```
user = User.query.get(3)
db.session.delete(user)
db.session.commit()

```



sqlalchemy混合查询

```
from sqlalchemy import or_

rule = or_(User.nickname.ilkie("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
query = User.query
query= query.filter(rule)
```



mysql事务

```
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
tmp_food_list = db.session.query(Food).filter(Food.id.in_(foods_id)).with_for_update().all()
```



sqlalchemy异常模块

```
from sqlalchemy.exc import InteqrityError
```

