from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='sign-up'),
    path('logout/', views.logout_view, name='logout'),
    path('action/check-username', views.check_username, name='check-username'),
    path('action/check-email', views.check_email, name='check-email'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password', views.change_password, name='change-password'),
    path('profile/manage-addresses', views.manage_addresses, name='manage-addresses'),
    path('profile/manage-addresses/add-address', views.add_address, name='add-address'),
    path('profile/manage-addresses/edit-address/<str:encoded_id>', views.edit_address, name='edit-address'),
    path('profile/manage-addresses/delete-address/<str:encoded_id>', views.delete_address, name='delete-address')
]

