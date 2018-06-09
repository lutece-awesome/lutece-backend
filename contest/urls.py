from django.urls import path
from . views import get_contest_list, create_contest, edit_contest, update_contest, overview_contest, get_contest_problem, get_problem_list

urlpatterns = [
    path( 'list/<int:page>/' , get_contest_list  , name = 'contest-list' ),
    path( 'create/contest/' , create_contest , name = 'contest-create' ),
    path( 'edit/<int:pk>/' , edit_contest , name = 'contest-edit'  ),
    path( 'update/<int:pk>/' , update_contest , name = 'contest-update' ),
    path( 'problem/<int:pk>/' , get_contest_problem , name = 'contest-problem' ),
    path( 'overview/<int:pk>/' , overview_contest , name = 'contest-overview' ),
    path( 'problem/list/<int:pk>/' , get_problem_list , name = 'contest-problem-list' )
]