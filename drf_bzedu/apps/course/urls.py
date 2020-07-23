from django.urls import path

from course import views

urlpatterns=[
    path('classify/',views.CourseClassifyListAPIView.as_view()),
    path('classifylist/',views.CourseListAPIView.as_view()),
    path('alllist/',views.CourseFilterListAPIView.as_view()),
    path('detail/<str:pk>',views.OneCourseAPIView.as_view()),
    path('chapter/',views.CourseChapterAPIView.as_view())
]

