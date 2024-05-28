from django.urls import path, include
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.goto_login, name='login'),
    path('signup/', views.goto_signup, name='sign-up')
]