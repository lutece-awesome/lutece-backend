from django.urls import path
from .views import home_render

urlpatterns = [
    path( '' ,  home_render , name = 'home' )
]