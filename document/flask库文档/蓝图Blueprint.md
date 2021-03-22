# 蓝图Blueprint

蓝图

一个应用中或跨应用制作应用组件和支持通用的模式

蓝图的作用

不使用蓝图

![image-20200109134647385](C:\Users\jarvis\AppData\Roaming\Typora\typora-user-images\image-20200109134647385.png)

新建三个文件



```
# -*- coding:utf-8 -*-

from main import app

@app.route("/register")
def register():
    return "register page"


# -*- coding:utf-8 -*-
from main import app

@app.route("/get_goods")
def get_goods():
    return "goods page"
    
    
```

```
# -*- coding:utf-8 -*-

from flask import Flask
from goods import get_goods
from users import register
app = Flask(__name__)


@app.route("/")
def index():
    return "index page"



if __name__ == '__main__':
    print(app.url_map)
    app.run()
```



![image-20200109134632855](C:\Users\jarvis\AppData\Roaming\Typora\typora-user-images\image-20200109134632855.png)



会出现循环导入的错误

![image-20200109134854606](C:\Users\jarvis\AppData\Roaming\Typora\typora-user-images\image-20200109134854606.png)

解决循环导入的方法



```
循环引用的解决方法，退出一方的模块导入时间，让另一方先导入。


```

另一种方法是用装饰器激进一点的方法

```
在主文件里来使用装饰器函数
app.route("/get_goods")(get_goods)
app.route("/register")(register)
```

```
def itcast(func):
    def inner(num):
        if num <= 18:
            func(num)
    return inner
    
@itcast
def get_goods(num):
    print(num)
    
get_goods(18)
>>>18
get_goods(20)
>>>


```

![image-20200109161622682](C:\Users\jarvis\AppData\Roaming\Typora\typora-user-images\image-20200109161622682.png)



```
def route(params):
	print(params)
	def decorator(func):
		def inner():
			func()
		return inner
	return decorator
	
In [40]: def route(params):
    ...:	print(params)
    ...:	def decorator(func):
    ...:		def inner():
    ...: 			func()
    ...: 		return inner
    ...:	return decorator

In [42]: @route("/get_goods")
    ...: def index():
    ...:     print("index")
    ...:
/get_goods

In [43]: index
Out[43]: <function __main__.route.<locals>.decorator.<locals>.inner()>

In [44]: index()
index

d = route("get_goods")(index)

```

![image-20200109163321445](C:\Users\jarvis\AppData\Roaming\Typora\typora-user-images\image-20200109163321445.png)



### 蓝图的使用

一、创建蓝图对象

```
# Blueprint必须指定两个参数，admin表示蓝图的名字，__name__表示蓝图所在模块
admin = Blueprint('admin', __name__)
```



二、注册蓝图路由

```
@admin.route("/")
def admin_index():
	return 'admin_index'
```



三、在程序实例中注册蓝图

```
app.register_blueprint(admin, url_prefix='/admin')
```



意味着是先让蓝图这个对象先保存视图函数的路由，之后在注册的时候再从蓝图对象里取出来，保存到全局url_map中去，这其实就是延时操作。





#### 以目录形式定义蓝图

![image-20200109172026484](C:\Users\jarvis\AppData\Roaming\Typora\typora-user-images\image-20200109172026484.png)

在\_\_init\_\_\.py文件里可以实例化蓝图对象，

```
# -*- coding:utf-8 -*-

from flask import Blueprint


app_cart = Blueprint('app_cart', __name__, template_folder='templates', static_folder='static')
print(__name__)

# 在__init__文件被执行的时候，把视图加载进来，让蓝图与应用程序知道有视图的存在

from .views import get_cart
```



#### 蓝图里模板目录的处理

在蓝图里也可以定义子模板目录和子静态文件目录，而主目录里的模板目录和静态目录优先于子目录。

```
app_cart = Blueprint('app_cart', __name__, template_folder='templates', static_folder='static')
```



