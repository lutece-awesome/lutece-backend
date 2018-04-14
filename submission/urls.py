from django.urls import path
from .views import submit_solution


urlpatterns = [
    path('submit/', submit_solution , name='submission-submit-solution'),
]
