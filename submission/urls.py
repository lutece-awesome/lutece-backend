from django.urls import path
from .views import submit_solution,fetch_waiting_submission


urlpatterns = [
    path('submit/', submit_solution , name='submission-submit-solution'),
    path('fetch/judge/', fetch_waiting_submission ),
    path('status/all/', submit_solution , name='submission-status-all'),
]