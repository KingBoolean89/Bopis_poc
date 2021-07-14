from django.contrib import admin
from .models import *



class RoleAdmin(admin.ModelAdmin):
    fields = ['name','resources']

admin.site.register(Role, RoleAdmin)