flask-sqlacodegen教程

安装：

```
pip install flask-sqlacodegen -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

使用：

```
flask-sqlacodegen 'mysql://root:mysql0220@127.0.0.1/food_db' --tables app_access_log --outfile "common/models/log/AppAccessLog.py" --flask
```



wx小程序的用户表

```
flask-sqlacodegen 'mysql://root:mysql0220@127.0.0.1/food_db' --tables member --outfile "common/models/member/Member.py" --flask
```

```
flask-sqlacodegen 'mysql://root:mysql0220@127.0.0.1/food_db' --tables user --outfile 'common/models/user.py' --flask

flask-sqlacodegen 'mysql://root:mysql0220@127.0.0.1/food_db' --tables food_sale_change_log --outfile 'common/models/food/FoodSaleChangeLog.py' --flask
```

```
flask-sqlacodegen 'mysql://root:myl0220@127.0.0.1/food_db' --tables member_cart --outfile "common/models/member/MemberCart.py" --flask

```

