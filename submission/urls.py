from django.urls import path
from .views import submit_solution,fetch_waiting_submission,get_status_all


urlpatterns = [
    path('submit/', submit_solution , name='submission-submit-solution'),
    path('fetch/judge/', fetch_waiting_submission ),
    path('status/all/<int:page>/', get_status_all , name='submission-status-list'),
]