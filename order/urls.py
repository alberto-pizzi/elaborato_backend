from django.urls import path, include
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('action/add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('action/remove-from-cart', views.remove_from_cart, name='remove-from-cart'),
    path('cart-overview/', views.cart_overview, name='cart-overview'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:id>/', views.order_detail, name='order-detail')

]