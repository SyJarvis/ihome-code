# 数据库migrate扩展的使用

### 数据库迁移

在开发过程中，需要修改数据库模型，而且还要在修改之后更新数据库。最直接的方式就是删除旧表，但这样会丢失数据。

更好的解决办法是使用数据库迁移框架，它可以追踪数据库模式的变化，然后把变动应用到数据库中。

在Flask中可以使用flask-migrate扩展，来实现数据迁移。并且集成到flask-script中，所以



为了导出数据库迁移命令，flask-migrate提供了一个migratecommand类，可以附加到flask-manager对象上。

首先要在虚拟环境下安装flask-migrate

```
pip install flask-migrate
```

```
# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager

app = Flask(__name__)

manager = Manager(app)

app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql+mysqlconnector://root:mysql0220@127.0.0.1:3306/test3?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# 第一个参数是Flask实例，第二个参数是sqlalchemy数据库实例
migrate = Migrate(app, db)

# manager是flask-script的实例，这条语句在flask-script中添加一个db命令
manager.add_command('db', MigrateCommand)

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

if __name__ == '__main__':
    manager.run()
```



初始化

```
python db_migrate db init
```

迁移

```
python db_migrate db migrate
```

升级

```
python db_migrate db upgrade
```

