from django.urls import path, include
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart', views.addToCart, name='add-to-cart'),
    path('remove-from-cart', views.removeFromCart, name='remove-from-cart')
]