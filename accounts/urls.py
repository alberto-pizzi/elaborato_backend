from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='sign-up'),
    path('logout/', views.logout_view, name='logout'),
    path('action/check-username', views.check_username, name='check-username'),
    path('action/check-email', views.check_email, name='check-email')
]

