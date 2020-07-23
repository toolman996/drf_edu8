from rest_framework.generics import ListAPIView
from home.models import Banner, Navbar
from home.serializers import BannerModelSerializer, NavbarModelSerializer
from drf_bzedu.settings.count import BANNER_COUNT,NAVBAR_COUNT

# 轮播图类视图
class BannerShow(ListAPIView):
    queryset = Banner.objects.filter(is_show=True,is_delete=False).order_by('-orders')[:BANNER_COUNT]
    serializer_class = BannerModelSerializer

# 导航栏类视图
class NavbarShow(ListAPIView):
    queryset = Navbar.objects.filter(is_show=True,is_delete=False).order_by('-orders')
    serializer_class = NavbarModelSerializer

# class NavbarButs(ListAPIView):
#     queryset = Navbar.objects.filter(is_show=True,is_site=True).order_by('-orders')
#     serializer_class = NavbarBut











