from django.contrib import admin
from .models import *



class ResourceAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Resource, ResourceAdmin)