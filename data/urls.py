from django.urls import path

from data.views import fetch_data

urlpatterns = [
    path('fetch/', fetch_data),
]
