from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns=[
    path('login/',obtain_jwt_token),
    path('captcha/',views.Captcha.as_view()),
    path('register/',views.Register.as_view()),
    path('check/<str:phone_id>',views.CheckPhoneId.as_view()),
    path('sms/<str:mobile>',views.SmsAPIView.as_view()),
]