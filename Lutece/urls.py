"""Lutece URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from markdownx import urls as markdownx
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .base_setting import DEBUG as lutece_debug

urlpatterns = [
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))
         ) if lutece_debug else path('graphql', GraphQLView.as_view(graphiql=False)),
    path('admin/', admin.site.urls),
    path('data_server/', include('data_server.urls')),
    re_path(r'^.*$', ensure_csrf_cookie(TemplateView.as_view(template_name='frontend/dist/index.html'))),
]
