# coding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(DjangoUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'permission_granted', 'is_active', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    list_filter = ('permission_granted', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('permission_granted', 'is_active', 'is_staff',
                                       'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {'classes': ('wide',),
             'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm


admin.site.register(User, UserAdmin)
