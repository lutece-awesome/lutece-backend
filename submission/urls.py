from django.urls import path
from .views import submit_solution, get_status_list, get_status_detail , get_status_detail_json, get_activity_json

urlpatterns = [
    path( 'submit/', submit_solution , name='submission-submit-solution'),
    path( 'status/detail/<int:submission_id>/' , get_status_detail , name = 'submission-status-detail' ),
    path( 'status/request/<int:submission_id>/' , get_status_detail_json , name = 'submission-status-detail-data-json' ),
    path( 'status/list/<int:page>/', get_status_list , name='submission-status-list'),
    path( 'activity/json/<int:user_pk>/' , get_activity_json , name = 'submission-get-activity' )
]