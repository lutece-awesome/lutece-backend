from django.urls import path
from .views import problem_detail_view, problem_list_view, problem_edit_view, problem_update_view

urlpatterns = [
    path('detail/<int:problem_id>/', problem_detail_view, name='problem-detail-view'),
    path('edit/<int:problem_id>/', problem_edit_view, name='problem-edit-view'),
    path('update/<int:problem_id>/' , problem_update_view , name = 'problem-update-view' ),
    path('list/<int:page>/', problem_list_view, name='problem-list-view')
]
