from django.urls import path, include
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart', views.remove_from_cart, name='remove-from-cart')
]