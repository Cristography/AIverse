"""
Django Admin configuration for Users app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['bio', 'avatar', 'website', 'location', 'theme', 'language', 'total_prompts', 'total_bookmarks']
    readonly_fields = ['total_prompts', 'total_bookmarks']


# Unregister the default User admin
admin.site.unregister(User)

# Register User with Profile inline
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]