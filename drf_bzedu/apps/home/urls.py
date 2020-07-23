from django.urls import path

from home import views

urlpatterns = [
    path("banner/", views.BannerShow.as_view()),
    path("navbar/", views.NavbarShow.as_view()),
    # path("navbars/", views.NavbarButs.as_view()),
]
