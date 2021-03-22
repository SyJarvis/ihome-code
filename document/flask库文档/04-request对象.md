# 04-request对象

### 4.3获取请求参数

from flask import request

就是Flask中表示当前请求的request对象，request对象中保存了一次HTTP请求的一切信息



**request常用的属性如下:**

| 属性    | 说明                   | 类型           |
| ------- | ---------------------- | -------------- |
| data    | 记录请求的数据         | *              |
| form    | 记录请求中的表单数据   | MultiDict      |
| args    | 记录请求中的查询参数   | MultiDict      |
| cookies | 记录请求中的cookie信息 | Dict           |
| headers | 记录请求中的报文头     | EnvironHeaders |
| method  | 记录请求使用的HTTP方法 | GET/POST       |
| url     | 记录请求的URL地址      | string         |
| files   | 记录请求上传的文件     | *              |

```
request.full_path
request.path
request.url
获取请求的json数据，返回字典
request.get_json()
```

postman软件



url参数不论是get还是post请求都可以使用，服务器端都可以接收参数。

headers可以当做字典，也可以用



### 4.3.1上传文件

已上传的文件存储在内存或是文件系统中一个临时的位置。你可以通过请求对象的files属性访问它们。每个上传的文件都会存储在这个字典里。它表现近乎为一个标准的Python对象，但它还有一个save()方法，这个方法允许你把文件保存到服务器的文件系统上。

```
<form action="/upload" method="post" enctype="multipart/form-data">
<input type="file" name="pic">
<input type="submit">
</form>
```

```
@app.route("/upload", methods=["POST"])
def upload():
    """接收前段传送过来的文件"""
    file_ojb = request.files.get("pic")
    if file_ojb is None:
        # 表示没有接收到数据
        return "未上传文件"

    # 将文件保存到本地
    # 1.创建一个文件
    f = open("./demo.jpg", "wb")
    # 2.写内容
    data = file_ojb.read()
    f.write(data)
    # 3.关闭文件
    f.close()
    return "上传成功"
```



如果你想知道上传前文件在客户端的文件名是什么，你可以访问filename属性。但是永远不要相信这个值，这个值使可以伪造的。如果你要把文件按客户端提供的文件名保存在服务器上，那么请把它传递给werkzeug提供的scure_filename()函数

```
'close', 'content_length', 'content_type', 'filename', 'he
aders', 'mimetype', 'mimetype_params', 'name', 'save', 'stream']
```



```
request.args
request.values
request.args
request.form
request.files
```



```

file_target = request.files

ImmutableMultiDict([('upfile', <FileStorage: 'home01.jpg' ('image/jpeg')>)])
2020-02-19 15:45:16,544 INFO sqlalchemy.engine.base.Engine ROLLBACK

```



```
# 获取ip地址
request.remote_addr
```