from django.urls import path
from . import views

urlpatterns = [
    path( '<int:problemId>/' , views.problemView , name = 'problemViewPage' )
]