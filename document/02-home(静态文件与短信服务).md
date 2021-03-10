### 自定义正则表达式

commons.py

```
# -*- coding: UTF-8 -*-

from werkzeug.routing import BaseConverter

# 定义正则转换器
class ReConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex
```

注册

```
ihome.__init__.py

from ihome.utils.commons import ReConverter
# 为flask添加自定义的转换器
app.url_map.converters["re"] = ReConverter
```



蓝图仅仅只是先把视图url等资源暂存起来，等app注册蓝图的时候，会统一调用这些资源函数。



### 静态文件的访问

在全局的flask的应用对象,app会有一个方法来专门返回静态文件的。

```
from flask import current_app
current_app.send_static_file(file_name)
```

```
# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app

# 提供静态文件的蓝图
html = Blueprint("web_html", __name__)

# 127.0.0.1:5000/
# 127.0.0.1:5000/index.html
# 127.0.0.1:5000/register.html
@html.route("/<re(r'.*'):html_file_name")
def get_html(html_file_name):
    """提供html文件"""
    if html_file_name:
        html_file_name = "html/" + html_file_name
    # flask提供的返回静态文件的方法
    return current_app.send_static_file(html_file_name)
```



### 图片验证码的流程

```
# 视图编写的流程
# 获取参数
# 校验参数
# 业务逻辑处理
# 返回值
```

验证码的url

```
# GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>
```

设置头有两种方式

```
1.make_response
2.
```

```
from flask import make_response
resp = make_response(image_data)
resp.headers["Content-Type"] = "image/jpg"
```





#### id的选择方式：

时间戳$(".phonecode-a").attr("onclick", "sendSMSCode();");

uuid	全局唯一标识符



短信验证码前段如何做出点击后显示出倒数60秒的样式

```
onclick="sendSMSCode"

进入点击事件之后，移除onclick事件
然后判断手机号是否填写，验证码是否填写
没有填写则---》$(".phonecode-a").attr("onclick", "sendSMSCode();");
数据校验完毕后发起ajax请求

```

```javascript
$.get("/api/v1.0/sms_codes/"+mobile, {image_code:imageCode, image_code_id:imageCodeId},
        function(data){
            if (0 != data.errno) {
                $("#image-code-err span").html(data.errmsg); 
                $("#image-code-err").show();
                if (2 == data.errno || 3 == data.errno) {
                    generateImageCode();
                }
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            }   
            else {
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒"); 
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码'); 
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60); 
            }
    }, 'json'); 
```

倒计时实现

```
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒"); 
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码'); 
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60); 
```

resp是后端返回的响应值，因为后端返回的是json字符串，

所以ajax帮助我们把这个json字符串转换为js对象，resp就是转换后的对象。

