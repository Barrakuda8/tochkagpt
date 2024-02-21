from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_login', 'first_name', 'last_name']
    exclude = ('groups', 'is_superuser', 'is_active', 'is_staff', 'user_permissions', 'password', 'username')

    list_display_links = ('id', 'username', 'first_name', 'last_name')
