from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    fields = ['email','username', 'password', 'groups', 'roles']

admin.site.register(User, UserAdmin)