# ihome登录逻辑

获取参数

校验参数

参数完整校验

手机号的格式

判断错误次数是否超过限制，如果超过限制，则返回

redis记录：”access_nums_请求的ip"

从数据库中根据手机号查询用户的数据对象，**判断是否有此用户**

用数据库的密码与用户填写的密码进行对比验证

​	如果验证失败，记录错误次数，返回信息

如果验证相同成功，保存登录状态，在session中



https://chriskiehl.com/article/thoughts-after-6-years





## 登录状态sessions



## 登录验证装饰器

```
定义的验证登录状态的装饰器
判断用户的登录状态
如果用户是登录的，执行视图函数
```





functools

```
import functools


def login_required(func):
    @functools.wraps(func)
    def wrapper(*arg, **kwargs):
        pass

    return wrapper

@login_required
def itcast():
    """itcast python"""
    pass

# itcast--->wrapper
print(itcast.__name__)
print(itcast.__doc__)
```

itcast的函数名和说明文档使用functools的装饰器就可以复制到wrapper函数对象里

```
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
```

