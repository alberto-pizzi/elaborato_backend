from django.contrib import admin

# Register your models here.
from .models import CustomUser,Address

from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm


class CustomUserAdmin(DefaultUserAdmin):
    #add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)})
    )
    readonly_fields = ('id','date_joined')

    list_display = ('id','username','email','first_name','last_name','is_staff','is_active','is_superuser','date_joined')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'email', 'first_name', 'last_name','is_active', 'is_staff', 'is_superuser',),
        }),
    )

admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(Address)
admin.site.unregister(Group)


