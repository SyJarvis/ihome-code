# ihome错误日志



日期：2020/2/1

问题：alembic.util.exc.CommandError: Can't locate revision identified by '076ef1b3b9e8'

原因：当前工程的migrations下有个alembic_version版本076ef1b3b9e8了，虽然你可能删掉migrations，但是数据库留有记录，需要删除。

解决办法：

​	删除数据库里的 alembic_version 表。

备注：也许你可以修改里面的值，



日期：2020/2/1

问题：alembic.util.exc.CommandError: Directory migrations already exists

原因：目录迁移已经存在



日期：2020/2/1

问题：alembic.util.exc.CommandError: Target database is not up to date.

原因：alembic.util.exc.CommandError:目标数据库不是最新的。

解决办法：

​	删除工程目录下的migrations目录，重新迁移文件。

