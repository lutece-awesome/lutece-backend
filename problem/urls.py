from django.urls import path
from .views import problem_view, problem_list

urlpatterns = [
    path('detail/<int:problemId>/', problem_view, name='problem_detailView'),
    path('list/<int:page>/', problem_list, name='problem_listView')
]
