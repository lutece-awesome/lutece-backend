from django.urls import path
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path( 'login/' , views.user_login , name = 'user_login' ),
    path( 'logout/' , views.user_logout , name = 'user_logout' )
]