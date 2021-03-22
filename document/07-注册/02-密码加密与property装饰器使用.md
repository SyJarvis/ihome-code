通常情况下，不会直接对用户输入的密码进行加密，而是通过加盐值之后再进行加密。salt值（随机字符串）

如果两个用户都输入相同的密码，但是因为添加的salt值不同，所以得到的秘钥也不同。



sha1与MD5已经被破解了，所以不安全了。被暴力测试给破解了，

现在sha256比较安全，因为它生成的密钥很长，破解起来时间会很长。

```
# 加上property装饰器后，会把函数变为属性，属性名即为函数名
@property
def password(self):
    """读取属性的函数行为"""
    # 函数的返回值会作为属性值传递
    # print(user.password)  # 读取属性时被调用
    # return "xxxx"
    raise AttributeError("这个属性只能设置，不能读取")
    
# 使用这个装饰器，设置属性 setter是设置器的意思
@password.setter
def password(self, value):
    """
    设置属性    user.password = "xxxxxx"
    :param value: 设置属性时的数据  value="xxxxxx",原始的明文密码
    :return:
    """
    self.password_hash = generate_password_hash(value)

```

