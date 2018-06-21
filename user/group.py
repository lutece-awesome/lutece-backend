from enum import Enum, unique
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
class _permission_meta:
    __slots__ = (
        'app_label',
        'model',
        'codename',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = [x for x in kw]

    def __str__(self):
        return self.app_label + ' ' + self.model + ' ' + self.codename

    def __repr__(self):
        return self.app_label + ' ' + self.model + ' ' + self.codename
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }

@unique
class _Permission( Enum ):
    CONTEST_ADD_CONTEST = _permission_meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'add_contest')
    CONTEST_CHANGE_CONTEST = _permission_meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'change_contest')
    CONTEST_VIEW_ALL = _permission_meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'view_all')
    CONTEST_HIDE_SUBMISSION = _permission_meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'hide_submission')
    PROBLEM_ADD_PPROBLEM = _permission_meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'add_problem')
    PROBLEM_CHANGE_PROBLEM = _permission_meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'change_problem')
    PROBLEM_VIEW_ALL = _permission_meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'view_all')
    PROBLEM_DOWNLOAD_DATA = _permission_meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'download_data')
    SUBMISSION_VIEW_ALL = _permission_meta(
        app_label = 'submission',
        model = 'submission',
        codename = 'view_all')
    USER_SET_NORMAL_USER= _permission_meta(
        app_label = 'user',
        model = 'user',
        codename = 'set_normal_user',)
    USER_SET_NORMAL_ADMIN = _permission_meta(
        app_label = 'user',
        model = 'user',
        codename = 'set_normal_admin',)
    USER_SET_SUPER_ADMIN = _permission_meta(
        app_label = 'user',
        model = 'user',
        codename = 'set_super_admin',)

    def set_permission( self , user ):
        content_type = ContentType.objects.get( app_label = self.value.app_label , model = self.value.model )
        user.user_permissions.add( Permission.objects.get( content_type = content_type , codename = self.value.codename ) )


class _group_meta:
    __slots__ = (
        'full',
        'display',
        'show',
        'show_in_userlist',
        'css',
        'url',
        'permission',
        '_field'
    )

    def needdisplay( self ):
        return hasattr( self , 'display' )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = [x for x in kw]

    def __str__(self):
        return self.full

    def __repr__(self):
        return str( self.full )
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }

@unique
class Group( Enum ):

    NORMAL_USER = _group_meta(
        full = 'normal_user',
        show = False,
        show_in_userlist = True,
        display = 'Normal User',
        url = 'user-set-normal-user',
        permission = [],
    )

    NORMAL_ADMIN = _group_meta(
        full = 'normal_admin',
        show = True,
        show_in_userlist = False,
        css = 'ui red ribbon label',
        display = 'Normal Admin',
        url = 'user-set-normal-admin',
        permission = ( _Permission.CONTEST_HIDE_SUBMISSION , _Permission.CONTEST_VIEW_ALL, _Permission.PROBLEM_ADD_PPROBLEM, _Permission.PROBLEM_CHANGE_PROBLEM , _Permission.PROBLEM_DOWNLOAD_DATA , _Permission.PROBLEM_VIEW_ALL , _Permission.SUBMISSION_VIEW_ALL )
    )

    SUPER_ADMIN = _group_meta(
        full = 'super_admin',
        show = True,
        show_in_userlist = False,
        css = 'ui green ribbon label',
        display = 'Super Admin',
        url = 'user-set-super-admin',
        permission = NORMAL_ADMIN.permission + ( _Permission.CONTEST_ADD_CONTEST , _Permission.CONTEST_CHANGE_CONTEST , _Permission.USER_SET_NORMAL_USER , _Permission.USER_SET_NORMAL_ADMIN )
    )

    ROOT = _group_meta(
        full = 'root',
        show = True,
        show_in_userlist = False,
        css = 'ui orange ribbon label',
        display = 'Super Root',
        permission = tuple( _Permission )
    )

def get_user_group( full ):
    for each in Group:
        if each.value.full == full:
            return each
    return None

def get_user_control_permission( group , target_user ):
    from django.urls import reverse
    USER_TYPE_PERMISSION = {
        _Permission.USER_SET_NORMAL_USER : Group.NORMAL_USER,
        _Permission.USER_SET_NORMAL_ADMIN : Group.NORMAL_ADMIN,
        _Permission.USER_SET_SUPER_ADMIN : Group.SUPER_ADMIN,
    }
    ret = list()
    for each in group.value.permission:
        if each in USER_TYPE_PERMISSION:
            ret.append( USER_TYPE_PERMISSION[each] )
    if get_user_group( target_user.group ) not in ret:
        return list()
    return ret
