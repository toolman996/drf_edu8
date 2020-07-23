from django.urls import path

from order import views

urlpatterns = [
    path('option/',views.GenerateOrderAPIView.as_view()),
]
