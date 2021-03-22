### flask库的类和函数

```
Flask对象
from flask import Flask

用法：
app = Flask(__name__)
```





### 蓝图

```
__init__.py
from flask import Blueprint


app_cart = Blueprint('app_cart', 
					__name__, 
					template_folder='templates', 
					static_folder='static')
print(__name__)

views.py
from . import app_cart
from flask import render_template

@app_cart.route("/")
def get_cart():
    return render_template("cart.html")
    
main.py
app.register_blueprint(app_cart, url_prefix='/cart')
```

