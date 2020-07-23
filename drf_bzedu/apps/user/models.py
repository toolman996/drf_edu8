
from django.db import models
from django.contrib.auth.models import AbstractUser

from course.BaseModel import BaseModel
from course.models import Course


class UserInfo(AbstractUser):
    """用户模型"""
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    user_head = models.ImageField(upload_to="user", verbose_name="用户头像", blank=True, null=True)

    class Meta:
        db_table = "tb_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

class UserCourse(BaseModel):
    """用户的课程购买记录"""
    pay_choices = (
        (1, '用户购买'),
        (2, '免费活动'),
        (3, '活动赠品'),
        (4, '系统赠送'),
    )
    user = models.ForeignKey(UserInfo, related_name='user_courses', on_delete=models.DO_NOTHING, verbose_name="用户")
    course = models.ForeignKey(Course, related_name='course_users', on_delete=models.DO_NOTHING, verbose_name="课程")
    trade_no = models.CharField(max_length=128, null=True, blank=True, verbose_name="支付平台的流水号",
                                help_text="将来依靠流水号到支付平台查账单")
    buy_type = models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="购买方式")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="购买时间")
    out_time = models.DateTimeField(null=True, blank=True, verbose_name="过期时间")

    class Meta:
        db_table = 'bz_user_course'
        verbose_name = '课程购买记录'
        verbose_name_plural = verbose_name
