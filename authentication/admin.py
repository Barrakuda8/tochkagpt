from django.contrib import admin
from .models import User, BusinessSubscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_login', 'first_name', 'last_name']
    exclude = ('groups', 'is_superuser', 'is_active', 'is_staff', 'user_permissions', 'password', 'username')

    list_display_links = ('id', 'username', 'first_name', 'last_name')


@admin.register(BusinessSubscription)
class BusinessSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'promo_code', 'balance', 'users']

    def users(self, obj):
        return obj.get_users()

    users.short_description = 'Пользователи'
