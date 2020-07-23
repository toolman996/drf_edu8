# 定义了jwt的返回值
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import UserInfo


def jwt_response(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id,
        # 'password':user.password
    }

def fun(args):
    try:
        result = UserInfo.objects.filter(Q(username=args) | Q(phone=args)).first()

    except UserInfo.DoesNotExist:
        return None
    else:
        return result

#多条件查询自定义认证方式
class UserAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        #多条件查询满足其一就可
        bt=fun(username)
        if bt and bt.check_password(password) and bt.is_authenticated:
            return bt
        else:
            return None


