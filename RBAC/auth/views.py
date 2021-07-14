import json
from passlib.hash import pbkdf2_sha256
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from users.serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.hashers import check_password
import jwt
from common.utils import generate_access_token, generate_refresh_token, asset_permissions
from common.utils import asset_permissions
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        user = User.objects.filter(username=data['username']).first()
        username = data['username']
        email = data['email']
        password = data['password']
        password2 = data['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'})
            else:
                if len(password) < 6:
                    return Response({'error': 'Password must be at least 6 characters'})
                else:
                    user = User.objects.create_user(username=username, password=password)

                    user.save()
                    return Response({'success': 'User created successfully'})
        else:
            return Response({'error': 'Passwords do not match'})

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    print(data)
    password = data['password']
    print(password)
    user = User.objects.filter(username=data['username']).first()
    pass_check = check_password(password, user.password)
    response = Response()
    
    if (data['username'] is None) or (data['password'] is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    #Development password check
    if not pass_check:
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token_view(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    User = request.user
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(username=payload.get('username')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})
