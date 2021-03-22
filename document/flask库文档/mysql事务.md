mysql事务

```
begin;
select * from food where id =1 for update;
commit;

当一个事务没有提交commit,另一个事务里执行相同语句的话是会等待的	
```

