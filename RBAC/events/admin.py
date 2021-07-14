from django.contrib import admin
from .models import *



class EventAdmin(admin.ModelAdmin):
    fields = ['action', 'role', 'user', 'resource']

admin.site.register(Event, EventAdmin)