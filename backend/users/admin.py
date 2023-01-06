from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    empty_value_display = '-пусто-'
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'username', 'first_name',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = ('user', 'author',)
