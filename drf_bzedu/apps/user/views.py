import random
import re
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as ccokt
from rest_framework.generics import CreateAPIView

# 公钥私钥
from drf_bzedu.libs.geetest import GeetestLib
from drf_bzedu.settings import count
from user.models import UserInfo
from user.serializer import RegisterModelSerializer
from user.utils import fun
from utils.SMS import Sms

pc_geetest_id = "6f91b3d2afe94ed29da03c14988fb4ef"
pc_geetest_key = "7a01b1933685931ef5eaf5dabefd3df2"


# 获取极验验证码并验证
class Captcha(APIView):
    user_id = 0
    status = False

    # 获取验证码
    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        user = fun(username)
        if user is None:
            return Response({"message": "用户不存在"}, status=ccokt.HTTP_400_BAD_REQUEST)
        self.user_id = user.id

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        return Response(response_str)

    # 验证验证码
    def post(self, request, *args, **kwargs):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        # 判断用户是否存在
        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "成功"} if result else {"status": "ok"}
        return Response(result)


# 注册实现类
class Register(CreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = RegisterModelSerializer


# 检查手机号是否存在
class CheckPhoneId(APIView):
    def get(self, request, phone_id):
        # 判断手机号是否合法
        if not re.match(r"^((13[0-9])|(14[5,6,7,9])|(15[^4])|(16[5,6])|(17[0-9])|(18[0-9])|(19[1,8,9]))\d{8}$", phone_id):
            return Response({"message": "手机号格式不正确"}, status=ccokt.HTTP_400_BAD_REQUEST)
        user = fun(phone_id)
        if user is not None:
            return Response({"message": "手机号已经被注册"}, status=ccokt.HTTP_400_BAD_REQUEST)
        return Response({"message": "ok"})


# 手机发送验证码逻辑
class SmsAPIView(APIView):
    def get(self, request, mobile):
        # 第一步连接数据库
        redis_connection = get_redis_connection("sms_code")
        # 1.判断手机验证码是否在60s内发送过短信
        mobile_code = redis_connection.get("sms_%s" % mobile)
        if mobile_code is not None:
            return Response({"message": "您已经发送过短信了"}, status=ccokt.HTTP_400_BAD_REQUEST)
        # 2.生成随机的短信验证码
        code = "%06d" % random.randint(0, 999999)
        # 3. 将验证码保存到redis中
        redis_connection.setex("sms_%s" % mobile, count.SMS_EXPIRE_TIME, code)  # 60s不允许再发送
        redis_connection.setex("mobile_%s" % mobile, count.MOBILE_EXPIRE_TIME, code)  # 验证码的有效时间
        # 4. 调用方法  完成短信的发送
        try:
            from my_celery.send_message.tasks import send_message
            send_message.delay(mobile,code)
            # message = Sms(count.API_KEY)
            # message.send_message(mobile, code)
        except:
            return Response({"message": "短信发送失败"}, status=ccokt.HTTP_500_INTERNAL_SERVER_ERROR)
        # 5. 响应回去
        return Response({"message": "发送短信成功"}, status=ccokt.HTTP_200_OK)
