from django.urls import path
from .views import submit_solution, get_status_list, get_status_detail

urlpatterns = [
    path('submit/', submit_solution , name='submission-submit-solution'),
    path( 'status/detail/<int:submission_id>/' , get_status_detail , name = 'submission-status-detail' ),
    path('status/list/<int:page>/', get_status_list , name='submission-status-list'),
]
