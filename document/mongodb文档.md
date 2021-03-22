查看帮助:mongod -help

启动 sudo service mongod start

停止 sudo service mongod stop

重启 sudo service mongod restart

查看是否启动成功	ps aux | grep mongod

配置文件的位置：/etc/mongod.conf

日志的位置:/var/log/mongodb/mongod.log





mongodb的基础命令

database:

```
查看当前的数据库：db
查看所有的数据库：show dbs
切换数据库：use db_name
删除当前的数据库：db.dropDatabase()
```



集合

```
不手动创建集合
向不存在的集合中第一次加入数据时，集合会被创建出来
手动创建集合
db.createCollection(name, options)
db.createCollection("stu")
db.createCollection("sub", {capped:true, size:10})
参数capped：默认值为false表示不设置上限，值为true表示设置上限。
参数size：当capped值为true时，需要指定此参数，表示上限大小，当文档达到上限时，会将之前的数据覆盖，单位为字节。
查看集合：show collections
删除集合：db.集合名称.drop()
```



mongodb插入数据

* db.collection.insert({})	插入数据，_id存在就会报错
* db.collection.save({})  插入数据，_id存在会更新
* 