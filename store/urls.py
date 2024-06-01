from django.urls import path, include
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.goto_login, name='login'),
    path('signup/', views.goto_signup, name='sign-up'),
    path('cart-overview/', views.goto_cart, name='cart-overview'),
    path('product/<int:id>', views.product_detail, name='product-detail'),
    path('<str:gen>', views.store_view, name='gender-store')
]