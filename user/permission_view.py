from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from json import dumps

@permission_required( 'user.set_normal_admin' )
def set_normal_admin( request ):
    from .models import User
    from .group import Group
    ret = { 'status' : True, }
    user = User.objects.get( pk = int(request.POST.get( 'user' )) )
    user.set_group( Group.NORMAL_ADMIN )
    return HttpResponse( dumps( status ) , content_type = 'application/json' )

@permission_required( 'user.set_super_admin')
def set_super_admin( request )；
    from .models import User
    from .group import Group
    ret = { 'status' : True, }
    user = User.objects.get( pk = int(request.POST.get( 'user' )) )
    user.set_group( Group.SUPER_ADMIN )
    return HttpResponse( dumps( status ) , content_type = 'application/json' )