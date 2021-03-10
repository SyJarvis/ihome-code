# csrf机制



#### csrf验证机制的流程

```
浏览器一旦是发起post请求，服务端就会验证csrf，flask从cookie中获取一个csrf_token值，再从请求体中获取一个csrf_token的值，然后把两个值进行对比，如果两个值相同，则校验通过，进入到视图函数中执行，否则失败，终止请求，返回状态码404错误。
```



跨站伪造攻击

csrf的使用

```
from flask_wtf import CSRFProtect
# 为flask补充csrf防护机制
csrf = CSRFProtect()
csrf.init_app(app)
```

flask的csrf应用

```
from flask_wtf import csrf
# 生成csrf值
csrf_token = csrf.generate_csrf()
csrf_token = csrf.generate_csrf()
resp = make_response(current_app.send_static_file(html_file_name))
resp.set_cookie("csrf_token", csrf_token)
# 不能设置csrf_token有效期

```

