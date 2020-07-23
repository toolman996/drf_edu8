from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView,RetrieveAPIView
from course.models import CourseCategory, Course, CourseChapter
from course.pagination import CoursePageNumber
from course.serializer import CourseClassifyserializer, Coursesserializer, OneCourserSerializer, OneCourseChapter


#查询课程分类信息
class CourseClassifyListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True,is_delete=False).order_by('orders')
    serializer_class = CourseClassifyserializer

#查询课程列表信息
class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by('orders')
    serializer_class = Coursesserializer


class CourseFilterListAPIView(ListAPIView):
    """根据条件查询课程"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = Coursesserializer

    # 根据不同的分类id查询不同的课程
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)
    # 排序
    ordering_fields = ("id", "students", "price")
    # 分页   只能有一个
    pagination_class = CoursePageNumber


class OneCourseAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = OneCourserSerializer


# 课程下对应的章节
class CourseChapterAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("orders",'id')
    serializer_class = OneCourseChapter
    # 根据课程id进行过滤筛选
    filter_backends = [DjangoFilterBackend]
    filter_fields=['course']




