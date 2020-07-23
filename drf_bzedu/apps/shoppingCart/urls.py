from django.urls import path

from shoppingCart import views

urlpatterns = [
    path('option/', views.ShoppingCartViewSet.as_view(
        {'post': 'add_shoppingcart', 'get': 'inquirt_cart',
         'patch': 'chanage_status', 'delete': 'delect','put':'revise_mfg'})),
    path('order/',views.ShoppingCartViewSet.as_view({'get':'pitch_shoppingcart'})),
]
