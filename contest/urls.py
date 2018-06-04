from django.urls import path
from . views import get_contest_list, create_contest, get_contest_detail, edit_contest

urlpatterns = [
    path( 'list/<int:page>/' , get_contest_list  , name = 'contest-list' ),
    path( 'create/contest/' , create_contest , name = 'contest-create' ),
    path( 'detail/<int:pk>/' , get_contest_detail , name = 'contest-detail' ),
    path( 'edit/<int:pk>/' , edit_contest , name = 'contest-edit'  )
]