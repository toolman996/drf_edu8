from rest_framework.serializers import ModelSerializer
from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


#课程分类序列化
class CourseClassifyserializer(ModelSerializer):
    class Meta:
        model=CourseCategory
        fields= ['id','name']



class CourseTeacherSerializer(ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "signature")
#课程分类序列化
class Coursesserializer(ModelSerializer):
    """课程列表"""

    # 序列化器嵌套查询老师信息
    teacher = CourseTeacherSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list",'activities_name','true_price']


class OneCourseTeacherSerializer(ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "image", "signature",'role','brief')
class OneCourserSerializer(ModelSerializer):
    teacher=OneCourseTeacherSerializer()
    class Meta:
        model=Course
        fields= ['id','name','teacher','brief_html','course_img','students','level_title',
                 'lessons','pub_lessons','price','video',
                 'activities_name','true_price','surplus_time']



class OneCourseLesson(ModelSerializer):
    class Meta:
        model=CourseLesson
        fields=('id','free_trail','name')
class OneCourseChapter(ModelSerializer):
    coursesections=OneCourseLesson(many=True)
    class Meta:
        model=CourseChapter
        fields=('id','chapter','name','coursesections')