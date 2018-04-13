from django.urls import path
from .views import problem_detail_view, problem_list_view

urlpatterns = [
    path('detail/<int:problemId>/', problem_detail_view, name='problem-detail-view'),
    path('list/<int:page>/', problem_list_view, name='problem-list-view')
]
