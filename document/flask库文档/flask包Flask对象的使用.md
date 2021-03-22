flask包Flask对象的使用



```
# 指定配置文件
app.config.from_pyfile('config.py')
# 传递模板函数	函数、名称
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
```



```
from flask import Flask

class Application(Flask):

    def __init__(self, import_name, template_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder)
        self.config.from_pyfile('config/base_setting.py')
        if 'ops_config' in os.environ:
            self.config.from_pyfile('config/%s_setting.py'%os.environ['ops_config'])

        db.init_app(self)

app = Application(__name__, template_folder=os.getcwd() + "/web/templates")

```



```
from flask import Flask
from flask import Blueprint, send_from_directory

# 返回静态文件,js,css,png
send_from_directory
```

