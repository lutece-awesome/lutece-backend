from django.urls import path
from .views import submit_solution, fetch_waiting_submission, get_status_list, Modify_submission_status


urlpatterns = [
    path('submit/', submit_solution , name='submission-submit-solution'),
    path('fetch/judge/', fetch_waiting_submission ),
    path( 'modify/judge/' , Modify_submission_status ),
    path('status/list/<int:page>/', get_status_list , name='submission-status-list'),
]
