from django.urls import path
from . import views

urlpatterns = [
    path( 'detail/<int:problemId>/' , views.problemView , name = 'problem_detailView' ),
    path( 'list/<int:page>/' , views.problemList , name = 'problem_listView' )
]