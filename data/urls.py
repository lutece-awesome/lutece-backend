from django.urls import path
from .views import fetch_data


urlpatterns = [
    path( 'fetch/' , fetch_data ),
]