from django.urls import path
from django.contrib.auth import authenticate

urlpatterns = [
    path( 'login/' , authenticate , name = 'user_login' ),
]