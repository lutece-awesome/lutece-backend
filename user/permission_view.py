from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from json import dumps
from .group import get_user_control_permission, get_user_group

@permission_required( 'user.set_normal_user' )
def set_normal_user( request ):
    from .models import User
    from .group import Group
    ret = { 'status' : True, }
    user = User.objects.get( pk = int(request.POST.get( 'user' )) )
    if len( get_user_control_permission( get_user_group( request.user.group ) , user ) ) == 0:
        raise RuntimeError( 'Permission Denied' )
    user.set_group( Group.NORMAL_USER )
    return HttpResponse( dumps( ret ) , content_type = 'application/json' )

@permission_required( 'user.set_normal_admin' )
def set_normal_admin( request ):
    from .models import User
    from .group import Group
    ret = { 'status' : True, }
    user = User.objects.get( pk = int(request.POST.get( 'user' )) )
    if len( get_user_control_permission( get_user_group( request.user.group ) , user ) ) == 0:
        raise RuntimeError( 'Permission Denied' )
    user.set_group( Group.NORMAL_ADMIN )
    return HttpResponse( dumps( ret ) , content_type = 'application/json' )

@permission_required( 'user.set_super_admin')
def set_super_admin( request ):
    from .models import User
    from .group import Group
    ret = { 'status' : True, }
    user = User.objects.get( pk = int(request.POST.get( 'user' )) )
    if len( get_user_control_permission( get_user_group( request.user.group ) , user ) ) == 0:
        raise RuntimeError( 'Permission Denied' )
    user.set_group( Group.SUPER_ADMIN )
    return HttpResponse( dumps( ret ) , content_type = 'application/json' )