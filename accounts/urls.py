from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('signup/', views.signupView, name='sign-up'),
    path('logout/', views.logout_view, name='logout')
]

