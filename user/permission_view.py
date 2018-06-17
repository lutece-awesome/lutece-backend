from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

@permission_required( 'user.set_normal_admin')
def set_normal_admin( request , pk ):
    pass