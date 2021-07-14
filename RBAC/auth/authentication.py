import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):

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
           

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        user = User.objects.filter(pk=payload['id']).first()
        print(user.pk)
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        return (user, None)
