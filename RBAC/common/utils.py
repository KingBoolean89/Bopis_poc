import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions

User = get_user_model()

def generate_access_token(user):

    access_token_payload = {
        'id': user.pk,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=480),
        'iat': datetime.datetime.utcnow(),
    }
    print(access_token_payload)
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'id': user.pk,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token

def asset_permissions(user):
    assets = []
    user_obj = User.objects.filter(username=user.username).first()
    print(user_obj.groups)
    if user_obj.groups.filter(name = 'Store Manager').exists():
        assets = ['Inventory Lookup', 'BOPIS', 'Ship From Store']
    elif user_obj.groups.filter(name = 'Store Clerk').exists():
        assets = ['Inventory Lookup']
    else:
        return assets    
    return assets 

def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        print(authorization_header)
        if not authorization_header:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_header.split(' ')[1]
            print(access_token)
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            raise Exception(f'Error Decoding Token') 
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(pk=payload['id']).first()
        print(user)
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        # self.enforce_csrf(request)
        return (user, None)
