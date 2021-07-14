from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login),
    path('signup', SignupView.as_view()),
    path('refresh_token', refresh_token_view)
]