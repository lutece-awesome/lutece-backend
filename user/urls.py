from django.urls import path
from .views import user_login, user_logout, user_signup , user_detail

urlpatterns = [
    path('login/', user_login, name='user-login'),
    path('logout/', user_logout, name='user-logout'),
    path('signup/', user_signup, name='user-signup'),
    path('detail/<int:user_id>' , user_detail , name = 'user-detail'),
]
