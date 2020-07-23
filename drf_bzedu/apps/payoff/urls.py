from django.urls import path

from payoff import views

urlpatterns = [
    path('pay/',views.PayOffAPIView.as_view()),
    path('result/',views.PayOffSuccessAPIView.as_view()),
]
