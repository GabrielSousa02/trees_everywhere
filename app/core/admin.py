"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Last session'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class ProfileAdmin(admin.ModelAdmin):
    """Define the admin page for profiles."""
    ordering = ['user']
    list_display = ['user', 'user_joined']
    fieldsets = (
        [None, {'fields': ('user_about',)}],
    )
    readonly_fields = ['user_joined']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile, ProfileAdmin)
