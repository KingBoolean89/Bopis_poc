from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers
from .models import *
from resources.serializers import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'resources'
            
        )
        depth = 3

class RoleAccessSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True)
    has_access = serializers.BooleanField()
    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'resources',
            'has_access'
        )
        depth = 3
