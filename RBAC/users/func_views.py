import sys
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from .models import *
from roles.serializers import *
from roles.models import *
from resources.serializers import *
from resources.models import *
from auth.permissions import IsAuthenticated
from common.pagination import CustomPagination

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_all_roles(request, userid):
    try:
        found_user = User.objects.get(pk=userid)
        print(found_user)
        found_user.roles.clear()
        return JsonResponse({"success": 1})
    except:
        return HttpResponse(status=400) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_user_resources(request, userid):
    print('hit')
    try:
        user = User.objects.get(pk=userid)
        print(user)
        roles = user.roles.values()
        resource_list = []
        role_list = []
        for role in roles:
            role_list.append(role)
            resources = list(Resource.objects.filter(roles__name=role['name']))
            for resource in resources:
                resource_list.append(resource)
        print(resource_list)
        print(role_list)
        new_list = list(dict.fromkeys(resource_list))
        paginator = CustomPagination()
        page = paginator.paginate_queryset(new_list, request)
        serializer = ResourceSerializer(page, many=True)
        return JsonResponse(serializer.data, safe=False)
    except:
        return HttpResponse(status=400)

@api_view(['DELETE','PATCH'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_users_role(request, userid, id):
    try:
        found_user = User.objects.get(pk=userid)
        print(found_user)
        found_role = Role.objects.get(pk=id)
        print(found_role)
        found_user.roles.remove(found_role)
        return JsonResponse({"success": 1})
    except:
        return HttpResponse(status=400) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_user_roles(request, userid):
    try:
        found_user = User.objects.get(pk=userid)
        found_role = found_user.roles.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(found_role, request)
        serializer = RoleAccessSerializer(page, many=True)
        return JsonResponse(serializer.data, safe=False)
    except:
        return HttpResponse(status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def has_role_access(request, userid):
    data = []
    all_roles = list(Role.objects.all())
    found_user = User.objects.get(pk=userid)
    found_roles = list(found_user.roles.all())
    print(found_roles)
    print(all_roles)
    for role in all_roles:
        if role in found_roles:
            setattr(role, 'has_access', True)
            data.append(role)
        else:
            setattr(role, 'has_access', False)
            data.append(role)
    paginator = CustomPagination()
    context = paginator.paginate_queryset(data, request)
    serializer = RoleAccessSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def has_resource_access(request, userid):
    data = []
    resource_list = []
    all_resources = list(Resource.objects.all())
    user = User.objects.get(pk=userid)
    roles = list(user.roles.all())
    for role in roles:
        resources = list(Resource.objects.filter(roles__name=role.name))
        res = role.resources.all()
        for item in res:
            print(item)
            resource_list.append(item)
    for resource in all_resources:
        if resource in resource_list:
            setattr(resource, 'has_access', True)
            data.append(resource)
        else:
            setattr(resource, 'has_access', False)
            data.append(resource)
    print(resources)
    paginator = CustomPagination()
    context = paginator.paginate_queryset(data, request)
    serializer = ResourceAccessSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_all_user_access(request,id):
    data = []
    users = list(User.objects.all())
    users_with_role = list(User.objects.filter(roles__id=id))
    for user in users:
        if user in users_with_role:
            setattr(user, 'has_access', True)
            data.append(user)
        else:
             setattr(user, 'has_access', False)
             data.append(user)
    paginator = CustomPagination()
    context = paginator.paginate_queryset(data, request)
    serializer = UserAccessSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_all_user_by_resource(request,id):
    data = []
    users = list(User.objects.all())
    resource = Resource.objects.get(pk=id)
    users_with_resource = list(User.objects.filter(roles__resources__id=id))
    new_list = list(dict.fromkeys(users_with_resource))
    print(new_list)
    for user in users:
        if user in new_list:
            setattr(user, 'has_access', True)
            data.append(user)
        else:
             setattr(user, 'has_access', False)
             data.append(user)
    paginator = CustomPagination()
    context = paginator.paginate_queryset(data, request)
    serializer = UserAccessSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)
