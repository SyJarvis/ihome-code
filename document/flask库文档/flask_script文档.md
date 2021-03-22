flask_script文档

```
import flask_script
# https://flask-script.readthedocs.io/en/latest/
```



官方示例

```
from flask_script import Manager

from myapp import app

manager = Manager(app)

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()
```



```
from flask_script import Manager, Server

manager = Manager(app)
# 添加命令，runserver,指定webserver类，
manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=True, use_reloader=True))

manager.run()
```



使用

```
python manager.py runserver
```

