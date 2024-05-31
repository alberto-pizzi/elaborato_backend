from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='sign-up'),
    path('logout/', views.logout_view, name='logout')
]

