from django.urls import path
from . import views

urlpatterns = [
    path( 'detail/<int:problemId>/' , views.problemView , name = 'problemViewPage' ),
    path( 'list/<int:page>/' , views.problemList , name = 'getProblemViewList' )
]