from django.urls import path
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path( 'signin/' , TemplateView.as_view( template_name = 'signin.html'  ) , name = 'user_signin' ),
    path( 'login/' , views.user_login , name = 'user_login' )
]