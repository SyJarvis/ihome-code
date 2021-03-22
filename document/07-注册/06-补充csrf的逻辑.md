cookie:csrf_token=xxx

body:csrf_token=xxx



状态:post\put\delete



服务器

csrf验证机制：从cookie中获取一个csrf_token的值，从请求体中获取一个csrf_token的值，如果两个值相同，则检验通过，可以进入到视图函数中执行，如果两个值不相同，则检验失败，会向前端返回状态码400的错误



csrf_token的值放在body里是以form表单来提交的，在后端也是使用request.form来提取参数，那么如果不在body里就提取不了了？这个比较灵活，如果不放在表单里，可以放在请求头里，

```
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
headers:{
    "X-CSRFToken":  
},
```

```
document.cookie	一个字符串
\\b 单词边界

document.cookie.match("\\bcsrf_token=([^;]*)\\b")[1];
```

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

