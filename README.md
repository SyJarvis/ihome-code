# ihome

一个使用flask开发的前后端分离的网站，目前是在更新中。



#### 更新列表

1.项目目录结构搭建与数据迁移完成

### 运行
python manage.py runserver
python manage.py runserver -h 192.168.0.103 -p 8000


### 荣联云通讯
https://www.yuntongxun.com/


### 数据库导入
数据库名:ihome
1.area_facility.sql
进入mysql，use ihome,然后复制area_facility.sql文件的sql语句，粘贴到命令行



## art-template高性能JavaScript模板引擎
https://aui.github.io/art-template/zh-cn/index.html


##### 迁移数据库
```
python manage.py db init
python manage.py db migrate -m "init table"
python manage.py db upgrade
```


##### 账号密码
```
13811111112
123456
```


##### 启动celery
```
cd /home/jarvis/Desktop/ihome
celery -A ihome.tasks.task_sms worker -l info
```


python manage.py db migrate -m "add trade_no"
python manage.py db upgrade


支付宝是要收手续费的
费率是千分之六


update ih_order_info set id=43 where id=3;
