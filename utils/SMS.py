import requests

from drf_bzedu.settings import count


class Sms(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.message_api_url = count.SINGLE_SEND_URL

    def send_message(self, phone, code):
        """
        短信发送的实现
        :param phone: 前端传递的手机号
        :param code: 随机验证码
        :return:
        """
        params = {
            "apikey": self.api_key,
            'mobile': phone,
            # 'text': "【赵少博test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
            'text': "【毛信宇test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        # 可以发送http请求
        requests.post(self.message_api_url, data=params)


if __name__ == '__main__':
    message = Sms(count.API_KEY)
    message.send_message("13253633376", "123456")
