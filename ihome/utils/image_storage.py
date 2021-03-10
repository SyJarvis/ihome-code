# -*- coding: utf-8 -*-

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config

# 填写你的Access Key和　Secret Key
access_key = "uzc59bVURbUbazey9vrexXKocNKBUN8NuLijk57N"
secret_key = "-9lenw28jU2REojvGkcsEPWk5Nm9V2HIVqb5NKts"


def storage(file_data):
    """
    上传文件到七牛
    :param file_data: 要上传的文件数据（二进制流)
    :return:
    """
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = "ihome"

    # 生成上传Token,可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600) # 上传的空间，文件名，过期时间

    ret, info = put_data(token, None, file_data)

    if info.status_code == 200:
        # 表示上传成功, 返回文件名
        return ret.get("key")
    else:
        # 上传失败
        raise Exception("上传七牛失败")
    # print(info)
    # print("*"*10)
    # print(ret) # 字典

# if __name__ == '__main__':
#     with open("./1.png", "rb")as f:
#         file_data = f.read()
#         storage(file_data)

