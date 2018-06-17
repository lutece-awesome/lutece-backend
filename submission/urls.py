from django.urls import path
from .views import submit_solution, get_status_list, get_submission_detail, get_activity_json, get_submission_code

urlpatterns = [
    path( 'submit/', submit_solution , name='submission-submit-solution'),
    path( 'code/<int:pk>/' , get_submission_code , name = 'submission-code' ),
    path( 'detail/<int:pk>/' , get_submission_detail , name = 'submission-detail' ),
    path( 'status/list/<int:page>/', get_status_list , name='submission-status-list'),
    path( 'activity/json/<int:user_pk>/' , get_activity_json , name = 'submission-get-activity' ),
]