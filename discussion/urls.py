from django.urls import path
from .views import discussion_show, discussion_reply, discussion_change_visibility

urlpatterns = [
    path('show/<int:pk>/', discussion_show, name='discussion-show'),
    path('reply/', discussion_reply, name='discussion-reply'),
    path('visibility/', discussion_change_visibility, name='discussion-change-visibility'),
]