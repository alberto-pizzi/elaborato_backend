from django.urls import path, include
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.gotoLogin, name='login'),
    path('signup/', views.gotoSignup, name='sign-up')
]