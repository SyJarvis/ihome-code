# ihome09-个人信息

图片上传服务,七牛云



utils/image_storage.py

```
# -*- coding: utf-8 -*-

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config

# 填写你的Access Key和　Secret Key
access_key = "uzc59bVURbUbazey9vrexXKocNKBUN8NuLijk57N"
secret_key = "-9lenw28jU2REojvGkcsEPWk5Nm9V2HIVqb5NKts"


def storage(file_data):
    """
    上传文件到七牛
    :param file_data: 要上传的文件数据（二进制流)
    :return:
    """
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = "ihome"

    # 生成上传Token,可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600) # 上传的空间，文件名，过期时间

    ret, info = put_data(token, None, file_data)

    if info.status_code == 200:
        # 表示上传成功, 返回文件名
        return ret.get("key")
    else:
        # 上传失败
        raise Exception("上传七牛失败")
```





### 后端上传图片逻辑

装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取

获取图片

调用七牛上传图片

保存文件名到数据库

保存成功返回,

```
return jsonify(errno=RET.OK, errmsg="保存成功", data={"avatar_url": auatar_url})
```





### 前端上传图片逻辑

```
$(document).ready(function () {
    // 上传头像
    $('#form-avatar').submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();
        // 表单异步提交
        $(this).ajaxSubmit({
            url: '/api/v1.0/users/avatar',
            type: 'post',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0') {
                    var avatarUrl = resp.data.avatar_url;
                    $('#user-avatar').attr('src', avatarUrl);
                } else {
                    alert(resp.errmsg);
                }
            }
        });
    });

    // 获取用户信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '4104') {
            // 未登录，跳转到登陆界面
            location.href = '/login.html'
        } else if(resp.errno == '0') {
            // 有获取到用户信息
            $('#user-name').val(resp.data.name);
            if (resp.data.avatar) {
                $('#user-avatar').attr('src', resp.data.avatar);
            }
        }
    }, "json");
    
    // 修改用户名
    $('#form-name').submit(function (e) {
        // 阻止form表单的默认行为
        e.preventDefault();
        // 获取name值
        var name = $('#user-name').val();
        // 判断用户名是否为空
        if (!name) {
            alert('用户名不能为空！');
            return
        }
        // ajax 提交用户名
        $.ajax({
            url: '/api/v1.0/users/name',
            data: JSON.stringify({'name': name}),
            type: 'PUT',
            contentType: 'application/json',
            dataType: 'json',
            headers: {
                "X-CSRFToken": getCookie('csrf_token')
            },
            success: function (data) {
                if (data.errno == '0') {
                    $('.error-msg').hide();
                    showSuccessMsg();
                } else if (data.errno == '4001') {
                    $('.error-msg').show();
                } else if (data.errno == '4101') {
                    location.href = '/login.html';
                }
            }
        });

    });
});
```







5图片表单的使用说明，

