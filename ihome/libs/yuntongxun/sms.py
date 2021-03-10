# -*- coding: UTF-8 -*-

from ihome.libs.yuntongxun.CCPRestSDK import REST
from ronglian_sms_sdk import SmsSDK
import configparser
# from .CCPRestSDK import REST

#主帐号
accountSid = '8a216da86f9cc12f016fd18d3d4c1bda'

#主帐号Token
accountToken = '1d39ab94d587407cba0d206b8a7a96af'

#应用Id
appId = '8a216da86f9cc12f016fd18d3db21be1'

#请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'
# https://app.cloopen.com:8883
#请求端口 
serverPort = '8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id
   
#sendTemplateSMS(手机号码,内容数据,模板Id)

class CCP(object):

    # 用来保存对象的类属性
    instance = None
    def __new__(cls):
        # 判断CCP类有没有已经创建好的对象，如果没有，创建一个对象，并且保存
        # 如果有，则将保存的对象直接返回
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
        return cls.instance

    # def __init__(self):
    #     # 初始化REST_SDK
    #     self.rest = REST(serverIP, serverPort, softVersion)
    #     self.rest.setAccount(accountSid, accountToken)
    #     self.rest.setAppId(appId)

    def send_template_sms(self, to, datas, temp_id):
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # for k,v in result.items():
        #
        #     if k == 'templateSMS':
        #             for k, s in v.items():
        #                 print('%s:%s' % (k, s))
        #     else:
        #         print('%s:%s' % (k, v))
        # statusCode: 000000
        # smsMessageSid: ef54fe83cff248e1b8de16707e92ccc1
        # dateCreated: 20210205214128
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送成功
            return 0
        else:
            # 发送失败
            return -1


# if __name__ == '__main__':
#     ccp = CCP()
#     ret = ccp.send_template_sms("13824555872", ["你真帅", "5"], 1)
#     print(ret)


"""
from ronglian_sms_sdk import SmsSDK

accId = '容联云通讯分配的主账号ID'
accToken = '容联云通讯分配的主账号TOKEN'
appId = '容联云通讯分配的应用ID'

def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = '容联云通讯平台创建的模板'
    mobile = '手机号1,手机号2'
    datas = ('变量1', '变量2')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)
"""

class CCP2(object):
    instance = None
    def __new__(cls):
        # 判断CCP类有没有已经创建好的对象，如果没有，创建一个对象，并且保存
        # 如果有，则将保存的对象直接返回
        if cls.instance is None:
            obj = super(CCP2, cls).__new__(cls)
            obj.sdk = SmsSDK(accId=accountSid, accToken=accountToken, appId=appId)
            cls.instance = obj
        return cls.instance

    def send_template_sms(self, tid, mobile, datas):
        """
        :param tid: str 短信模板id ,    测试:1
        :param mobile: str 手机号码,mobile = '手机号1,手机号2'
        :param datas: tuple ('验证码', '几分钟')
        :return:
        """
        result = self.sdk.sendMessage(tid, mobile, datas)
        print("===========")
        print(result)
        print(type(result))
        result = dict(result)
        print("dictyssss")
        print(result)
        # result = dict(result)
        # status_code = result.get("StatusCode")
        # print(status_code)
        print("============")
        # if status_code == "000000":
        #     return 0
        # else:
        #     return -1



# if __name__ == '__main__':
#     ccp = CCP2()
#     tid = '1'
#     mobile = '13824555872'
#     datas = ('变量1', '变量2')
#     ccp.send_template_sms(tid, mobile, datas)



