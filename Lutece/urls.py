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
from graphene_file_upload.django import FileUploadGraphQLView
from .base_setting import DEBUG
from django.conf import settings
from django.conf.urls.static import static

if DEBUG:
    graphql = path('graphql', FileUploadGraphQLView.as_view(graphiql=True))
else:
    graphiql = []

urlpatterns = static( settings.MEDIA_URL , document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin.site.urls),
    path('data_server/', include('data_server.urls')),
    re_path(r'^.*$', TemplateView.as_view(template_name='static/index.html')),
] + graphql