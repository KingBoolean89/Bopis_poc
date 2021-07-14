from rest_framework import serializers
from .models import *
from users.serializers import *
from roles.serializers import *
from resources.serializers import *

class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = RoleSerializer()
    resource = ResourceSerializer()

    class Meta:
        model = Event
        fields = '__all__'