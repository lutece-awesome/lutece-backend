from django.urls import path
from .views import problem_discussion_show, problem_discussion_reply, discussion_change_visibility

urlpatterns = [
    path('show/<int:pk>/', problem_discussion_show, name='discussion-problem-show'),
    path('reply/<int:pk>/', problem_discussion_reply, name='discussion-problem-reply'),
    path('visibility/', discussion_change_visibility, name='discussion-change-visibility'),
]