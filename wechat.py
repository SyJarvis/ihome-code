# coding:utf-8

from flask import Flask, request, abort
import hashlib

# 常量
# 微信token令牌
WEHCAT_TOKEN = "itcast"


app = Flask(__name__)

@app.route("/wechat8000")
def wechat():
    """对接微信公众号服务器"""
    # 接收微信服务器发送的参数
    signature = request.args.get("signature")
    timestampe = request.args.get("timestampe")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    # 校验参数
    if not all([signature, timestampe, nonce, echostr]):
        abort(400)

    # 按照微信的流程进行计算签名
    #　字典序排序
    li = [WEHCAT_TOKEN, timestampe, nonce]
    # 排序
    li.sort()
    # 拼接
    tmp_str = "".join(li)
    # 进行sha1加密
    sign = hashlib.sha1(tmp_str).hexdigest()

    # 将自己计算的签名值与请求的签名参数进行对比，如果相同，则证明请求来自微信服务器
    if signature != sign:
        abort(403)
    else:
        return echostr

if __name__ == '__main__':
    app.run(port=8000, debug=True)



