from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
#     """Admin interface for User model"""
    list_display = ['username', 'email', 'is_superuser', 'is_active', 'created']
    list_filter = ['is_superuser','created']
