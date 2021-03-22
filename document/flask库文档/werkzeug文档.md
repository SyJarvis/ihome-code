```
# 获取一个安全的文件名
from werkzeug.utils import secure_filename
ext = filename.r

加密算法函数。
from werkzeug.security import generate_password_hash, check_password_hash
    def check_password(self, passwd):
        """
        校验密码的正确性
        :param passwd: 用户登录时填写的原始密码
        :return: 如果正确返回true，否则返回false
        """
        return check_password_hash(self.password_hash, passwd)

    def generate_password_hash(self, origin_password):
        """ 对密码进行加密"""
        self.password_hash = generate_password_hash(origin_password)
```