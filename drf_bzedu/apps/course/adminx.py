
import xadmin

from course import models
from course.models import Course, CourseCategory, CourseLesson, CourseChapter, Teacher


class CourseCategoryModelAdmin(object):
    """课程分类表"""
    pass


xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    """课程信息表"""
    pass


xadmin.site.register(Course, CourseModelAdmin)


class CourseChapterModelAdmin(object):
    """课程章节表"""
    pass


xadmin.site.register(CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    """课程课时表"""
    pass


xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


class TeacherLessonModelAdmin(object):
    """讲师表"""
    pass


xadmin.site.register(Teacher, TeacherLessonModelAdmin)




# 优惠相关
class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass


xadmin.site.register(models.CourseDiscountType, PriceDiscountTypeModelAdmin)


class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    pass


xadmin.site.register(models.CourseDiscount, PriceDiscountModelAdmin)


class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass


xadmin.site.register(models.CoursePriceDiscount, CoursePriceDiscountModelAdmin)


class ActivityModelAdmin(object):
    """商品活动模型"""
    pass


xadmin.site.register(models.Activity, ActivityModelAdmin)


class CourseExpireModelAdmin(object):
    """课程有效期模型"""
    pass


xadmin.site.register(models.CourseExpire, CourseExpireModelAdmin)





























































