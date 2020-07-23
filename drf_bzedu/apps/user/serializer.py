import re
# import random
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django_redis import get_redis_connection
from user.models import UserInfo
from user.utils import fun
from utils.random_name import get_random_name


class RegisterModelSerializer(ModelSerializer):
    token=serializers.CharField(max_length=888,read_only=True,help_text='token')
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")
    class Meta:
        model = UserInfo
        fields = ('id', 'password', 'phone', 'username','token','sms_code')

        extra_kwargs = {
            # 只参与序列化 'read_only': True
            'id': {
                'read_only': True
            },
            # 只参与序列化 'read_only': True
            'username': {
                'read_only': True
            },
            # 只参与反序列化 'write_only': True
            'password': {
                'write_only': True
            },
            # 只参与反序列化 'write_only': True
            'phone': {
                'write_only': True
            },
        }

    # 全局钩子验证手机号
    def validate(self, attrs):
        my_phone = attrs.get('phone')
        my_password = attrs.get('password')
        my_code=attrs.get('sms_code')
        # 正则验证手机号是否规范
        # if not re.match(r'^((13[0-9])|(14[5,6,7,9])|(15[^4])|(16[5,6])|(17[0-9])|(18[0-9])|(19[1,8,9]))\\d{8}$',my_phone):
        if not re.match(r'^((13[0-9])|(14[5,6,7,9])|(15[^4])|(16[5,6])|(17[0-9])|(18[0-9])|(19[1,8,9]))\d{8}$',
                        my_phone):
            raise serializers.ValidationError('手机号格式有误，请重新输入')
        # 验证手机号是否存在
        try:
            all_name = fun(my_phone)
        except:
            all_name = None
        if all_name:
            raise serializers.ValidationError('手机号已被注册，请重新输入')
            #验证手机号短信验证码是否正确
        redis_connection = get_redis_connection("sms_code")
        phone_code = redis_connection.get("mobile_%s" % my_phone)
        if phone_code.decode() != my_code:
            # 为了防止暴力破解 可以再次设置一个手机号只能验证 n次  累加
            raise serializers.ValidationError("验证码不一致")

            # 成功后需要将验证码删除
        return attrs

    # 重写create方法设置用户信息
    def create(self, validated_data):
        # get_list=['老王','常乐','明媚','张三','小白']
        get_pwd = validated_data.get('password')
        phone = validated_data.get('phone')
        salt_pwd = make_password(get_pwd)
        username = get_random_name()
        # 添加数据
        result = UserInfo.objects.create(
            phone=phone,
            username=username,
            password=salt_pwd,
        )
        #注册成功后生成token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(result)
        result.token = jwt_encode_handler(payload)
        return result
