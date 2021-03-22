## 05-abort函数、自定义错误、视图函数的返回值

### abort函数

```
from flask import Flask, request, render_template, redirect, url_for, abort, Response

# 使用abort函数可以立即终止视图函数的执行
# 并可以返回给前段特定的信息
# 1 传递状态码信息，必须是标准的http状态码
# abort(403)
# 2.传递响应体信息
resp = Response("login failed")
abort(resp)
```





### 自定义异常处理

```
# 定义错误处理的方法
@app.errorhandler(404)
def handle_404_error(error):
    """自定义的处理错误方法"""
    # 这个函数的返回值会是用户看到的最终结果

    return u"出现了404错误，错误信息：%s"%error
```



### 设置响应信息的方法

```
@app.route("/index")
def index():
    # 1 使用元组，返回自定义的响应信息
    # 响应体   状态码     响应头
    return ("index page", 400, [("Itcast", "python"), ("City", "shenzhen")])
```



```
Request URL:http://127.0.0.1:5000/index
Request Method:GET
Status Code:400 BAD REQUEST
Remote Address:127.0.0.1:5000
Response Headers
view source

City:shenzhen
Content-Length:10
Content-Type:text/html; charset=utf-8
Date:Sat, 28 Dec 2019 10:58:58 GMT
Itcast:python
Server:Werkzeug/0.16.0 Python/3.5.2
```



### 返回json数据

```
from flask import Flask, jsonify
import json
app = Flask(__name__)


@app.route("/index")
def index():
    # tornado
    # json就是字符串
    # json.dumps(dict)  将python的字典转为json字符串
    # json.loads(str)   将字符串转换为python中的字典
    data = {
        "name":"python",
        "age": 24
    }
    # json_str = json.dumps(data)
    #
    # return json_str, 200, {"Content-Type": "application/json"}
    return jsonify(data)
```

