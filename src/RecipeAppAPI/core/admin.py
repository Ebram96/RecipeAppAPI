from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserProfileAdmin(BaseUserAdmin):
    """Represents the django admin customizations for our custom user model"""
    ordering = ["id"]
    list_display = ["email", "name"]


admin.site.register(models.UserProfile, UserProfileAdmin)
