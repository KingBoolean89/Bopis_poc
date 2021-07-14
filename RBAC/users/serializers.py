from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'roles',
        ]
        depth = 3

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

   
class UserAccessSerializer(serializers.ModelSerializer):
    has_access = serializers.BooleanField()    
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'roles',
            'has_access'
            ]
        depth = 3