from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from users.serializers import *
from roles.serializers import *
from .models import *
from roles.models import *
from auth.permissions import IsAuthenticated
from common.pagination import CustomPagination
from django.core.exceptions import ObjectDoesNotExist
import sys
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_all_resources_access(request,id):
    data = []
    role = Role.objects.get(pk=id)
    resources = list(Resource.objects.all())
    resources_with_role = role.resources.all()
    print(resources_with_role)
    for resource in resources:
        if resource in resources_with_role:
            setattr(resource, 'has_access', True)
            data.append(resource)
        else:
             setattr(resource, 'has_access', False)
             data.append(resource)
    paginator = CustomPagination()
    context = paginator.paginate_queryset(data, request)
    serializer = ResourceAccessSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def can_delete_resource(self, id):
    try:
        resource = Resource.objects.get(pk=id)
        roles = list(Role.objects.all())
        roles_with_resource = list(Role.objects.filter(resources__id=id))
        print(roles_with_resource)
        if not roles_with_resource:
            response = {
                'Response': True
            }
        else:
            response = {
                'Response': False
            }
        return Response(data=response) 
    except ObjectDoesNotExist:
        return JsonResponse({"error": 'Object Does Not Exist'})     
    except:
        print("Unexpected errors:", type(sys.exc_info()), sys.exc_info())
        return JsonResponse({"error": str(sys.exc_info())})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def check_resource_permission(self, userid, id):
    data = []
    all_roles = list(Role.objects.all())
    user = User.objects.get(pk=userid)
    roles = list(user.roles.all().values('id'))
    resource = Resource.objects.get(pk=id)
    roles_with_resource = list(Role.objects.filter(resources__name=resource.name).values('id'))
    print(roles_with_resource)
    print(roles)
    check =  any(item in roles_with_resource for item in roles)
    if check is True:
        response = {
            "Response":True
        }
    else:
        response = {
            "Response":False
        }
    return Response(data=response)