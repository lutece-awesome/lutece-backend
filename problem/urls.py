from django.urls import path
from .views import problem_detail, problem_list, problem_edit, problem_update, search, problem_upload_data, problem_create_check

urlpatterns = [
    path('detail/<int:problem_id>/', problem_detail, name='problem-detail'),
    path('edit/<int:problem_id>/', problem_edit, name='problem-edit'),
    path('update/<int:problem_id>/' , problem_update , name = 'problem-update' ),
    path('list/<int:page>/', problem_list, name='problem-list'),
    path('upload/data/<int:problem_id>' , problem_upload_data , name = 'problem-upload-data' ),
    path('search/<str:til>/' , search , name = 'problem-search' ),
    path('create/check/' , problem_create_check , name = 'problem-create-check' ),
]