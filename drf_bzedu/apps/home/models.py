from django.db import models
from home.BaseModel import BaseModel
# Create your models here.

# banner轮播图模型
class Banner(models.Model):
    img = models.ImageField(upload_to="banner", max_length=255, verbose_name="轮播图图片")
    title = models.CharField(max_length=200, verbose_name="轮播图标题")
    link = models.CharField(max_length=300, verbose_name="图片链接")
    is_show = models.BooleanField(default=False, verbose_name="是否显示图片")
    orders = models.IntegerField(default=1, verbose_name="图片排序")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "tb_banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 导航栏模型
class Navbar(BaseModel):

    POSITION_OPTION = (
        (1, "顶部导航"),
        (2, "底部导航"),
    )
    title = models.CharField(max_length=200, verbose_name="导航标题")
    link = models.CharField(max_length=300, verbose_name="导航链接")
    position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name="导航位置")
    is_site = models.BooleanField(default=False, verbose_name="是否是外部链接")

    class Meta:
        db_table = "tb_navbar"
        verbose_name = "导航栏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title