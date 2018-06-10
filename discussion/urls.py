from django.urls import path
from .views import show_discussions

urlpatterns = [
    path('show/<int:pk>/', show_discussions, name='show-discussions'),
]