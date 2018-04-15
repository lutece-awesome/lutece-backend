from django.urls import path
from .views import submit_solution


urlpatterns = [
    path('solution/', submit_solution , name='submit-solution'),
]
