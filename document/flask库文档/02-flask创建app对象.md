flask创建app对象



初始化参数

```
from flask import Flask
import_name		导入路径(需找静态目录与模板目录位置的参数)
static_url_path	静态文件url访问路径
static_folder	静态文件目录的存放路径	'static'
template_folder:	模板文件目录存放路径	'templates'
```

配置参数

```
app.config.from_Pyfile("config.cfg")
app.config.from_object(obj)

```



读取配置参数

```
from flask import current_app
current_app	是你创建出的Flask对象的app的全局代理人

app.config.get("ITCAST")

current_app.config.get("ITCAST")
```

