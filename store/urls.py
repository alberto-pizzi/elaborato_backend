from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.goto_login, name='login'),
    path('signup/', views.goto_signup, name='sign-up')
]