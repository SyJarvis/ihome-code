### 设置cookie

```
from flask import Flask, make_response, request

resp = make_response("success")
# 设置cookie，并设置有效期,max_age，单位s
resp.set_cookie("Itcast", "Python", max_age=20)
# 用headers来设置cookie
resp.headers["Set_sookie"] = "Itcast3=Python3"
# 获取cookie
c = request.cookies.get("Itcast")
# 删除cookie
resp = make_response("del success")
resp.delete_cookie("Itcast3")
```

flask的sesssion需要用到秘钥

flask默认把session保存到cookie中



flask用到秘钥是为了防止篡改session的数据，把秘钥和数据混合起来，以达到混淆的效果。

cookie保存到用户浏览器，而session会话的数据保存到服务器上的，



因为一些隐私法律的原因，用户有权选择网站是否可以使用cookie,所以当用户拒绝使用cookie的时候，你需要把session_id放到get请求参数里传递到用户浏览器。

session的会话数据可以保存到数据库、程序内存、缓存库.

### 设置session

session广义上：机制

session狭义上：保存到服务器中的session数据

```
# -*- coding:utf-8 -*-

from flask import Flask, session
import json
app = Flask(__name__)

# flask的session需要用到的秘钥字符串
app.config["SECRET_KEY"] = "dnshsjskdjdhdkddkssdkjdkjsskss"

@app.route("/login")
def login():
    # 设置session数据
    session["name"] = "Python"
    session["mobile"] = "1861111111"
    return "login success"

@app.route("/index")
def index():
    # 获取session数据
    name = session.get("name")
    return "Hello %s" % name


if __name__ == '__main__':
    app.run(debug=True)
```

