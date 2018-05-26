from django.urls import path
from .views import problem_detail_view, problem_list_view, problem_edit_view, problem_update_view, problem_create_view, search_view, problem_upload_data_view, problem_create_check_view

urlpatterns = [
    path('detail/<int:problem_id>/', problem_detail_view, name='problem-detail-view'),
    path('edit/<int:problem_id>/', problem_edit_view, name='problem-edit-view'),
    path('update/<int:problem_id>/' , problem_update_view , name = 'problem-update-view' ),
    path('create/' , problem_create_view , name = 'problem-create-view' ),
    path('list/<int:page>/', problem_list_view, name='problem-list-view'),
    path('upload/data/<int:problem_id>' , problem_upload_data_view , name = 'problem-upload-data-view' ),
    path('search/<str:til>/' , search_view , name = 'problem-search-view' ),
    path('create/check/' , problem_create_check_view , name = 'problem-create-check-view' ),
]