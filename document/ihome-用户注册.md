# ihome-用户注册

用户注册逻辑

1. 获取请求的json数据，返回字典
2. 校验参数
3. 判断手机号格式，　格式不对－－－>
4. 判断两次密码是否一致
5. 从redis中取出短信验证码
6. 判断短信验证码是否过期
7. 删除redis中的短信验证码，防止重复使用校验
8. 判断用户填写短信验证码的正确性
9. 判断用户的手机号是否已注册，如果已注册，则跳转到登录页
10. 保存用户的注册数据到数据库中
11. 保存登录状态到session中
12. 返回结果



```
sqlalchemy.exc
from sqlalchemy.exc import IntegrityError
封装了所有sql
```







## 02密码加密与property装饰器使用

password = "1234567"

直接对password进行sha1加密也不安全

要加盐值，salt值，用来混淆

用户1 password="123456" + "abc"	sha1		abc$hxosifodsjsjsijsjssa

用户2 password="123456" + "def"	sha1		def$dfekjsksksksksksks



加密算法

已被攻破sha1	md5

还算安全sha256



```
werkzeug
Werkzeug是一个WSGI工具包，他可以作为一个Web框架的底层库。
https://werkzeug-docs-cn.readthedocs.io/zh_CN/latest/
```

​	

类里面一共有三种方法

对象方法

静态方法

类方法

方法变为属性－－－装饰器

![image-20210210164447051](/home/jarvis/.config/Typora/typora-user-images/image-20210210164447051.png)







注册前端编写

ajax

```
        $.ajax({
            url:"/api/v1.0/users",
            type:'post',
            data:req_json,
            contentType: "application/json",
            dataType:'json',
            headers:{
              "X-CSRFToken":getCookie('csrf_token')
            },
            success:function(resp){
                if (resp.errno == "0"){
                    //注册成功，跳转主页
                    location.href = '/index.html';
                } else {
                    alert(resp.errmsg);
                }
            }
        })
```

request.form	表单格式

request.argv	get请求参数

request.data	除了表单格式都可以



如果请求体的数据不是表单格式，可以将csrf_token的值放到请求头中：X-CSRFToken

```
document.cookie
document.cookie.match("\\bcsrf_token=([^;]*)\\b")[1];

```

