from rest_framework import serializers
from .models import *

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id','name')
        depth = 3

class ResourceAccessSerializer(serializers.ModelSerializer):
    has_access = serializers.BooleanField()
    class Meta:
        model = Resource
        fields = ('id','name','has_access')
        depth = 3