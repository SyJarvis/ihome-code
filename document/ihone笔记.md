# ihone笔记

```
>>> import random
>>> random.randint(0, 999999)
961824
>>> "%06d"%random.randint(0, 999999)
'840214'
>>> 
```

字符串格式化



可能出现异常的地方，就使用try-except

redis取出的数据为bytes

```
b'IAUW'
IAUW
```

```
b'IAUW'.decode()
```



防止对同一个图片验证码进行校验的逻辑



在redis中删除图片验证码数据就可以实现了，让用户下次用新的验证码来进行



FLUSHALL

