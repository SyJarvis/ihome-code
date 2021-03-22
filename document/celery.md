# celery

celery一个独立的第三方库，专门用来解决异步任务的，



发布任务的一方

django

flask



真正执行任务的一方worker

具备多任务处理

多进程(默认)

协程gevent\greenlet





broker任务队列

redis\mysql



error: VersionMismatch('Redis transport requires redis-py versions 3.2.0 or later. You have 2.10.5',)



```
--- ***** ----- 
-- ******* ---- Linux-4.15.0-29-generic-x86_64-with-Ubuntu-18.04-bionic 2021-03-16 10:57:42
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         ihome:0x7fd2b8f08ef0
- ** ---------- .> transport:   redis://127.0.0.1:6379/1
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 4 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . ihome.tasks.task_sms.send_sms

[2021-03-16 10:57:44,307: INFO/MainProcess] Connected to redis://127.0.0.1:6379/1
[2021-03-16 10:57:44,333: INFO/MainProcess] mingle: searching for neighbors
[2021-03-16 10:57:46,136: INFO/MainProcess] mingle: all alone
[2021-03-16 10:57:48,056: INFO/MainProcess] celery@ubuntu ready.

```

AssertionError: View function mapping is overwriting an existing endpoint function: api_1_0.get_user_houses