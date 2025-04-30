from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "language", "is_staff", "is_active")  # Fields to display in admin
    list_filter = ("language", "is_staff", "is_active")  # Filter options
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "language")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    search_fields = ("username", "email")  # Search users by name and email
    ordering = ("username",)

admin.site.register(CustomUser, CustomUserAdmin)

