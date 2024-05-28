from django.urls import path, include
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout')
]