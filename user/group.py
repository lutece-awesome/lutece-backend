from enum import Enum, unique
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

@unique
class _Permission( Enum ):
    class _meta:
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

    CONTEST_ADD_CONTEST = _meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'add_contest')
    CONTEST_CHANGE_CONTEST = _meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'change_contest')
    CONTEST_VIEW_ALL = _meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'view_all')
    CONTEST_HIDE_SUBMISSION = _meta(
        app_label = 'contest',
        model = 'contest',
        codename = 'hide_submission')
    PROBLEM_ADD_PPROBLEM = _meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'add_problem')
    PROBLEM_CHANGE_PROBLEM = _meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'change_problem')
    PROBLEM_VIEW_ALL = _meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'view_all')
    PROBLEM_DOWNLOAD_DATA = _meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'download_data')
    SUBMISSION_VIEW_ALL = _meta(
        app_label = 'submission',
        model = 'submission',
        codename = 'view_all')
    USER_SET_NORMAL_ADMIN = _meta(
        app_label = 'user',
        model = 'user',
        codename = 'set_normal_admin')
    USER_SET_SUPER_ADMIN = _meta(
        app_label = 'user',
        model = 'user',
        codename = 'set_super_admin')
    
    def set_permission( self , user ):
        content_type = ContentType.objects.get( app_label = self.value.app_label , model = self.value.model )
        user.user_permissions.add( Permission.objects.get( content_type = content_type , codename = self.value.codename ) )

@unique
class Group( Enum ):

    class _meta:
        __slots__ = (
            'full',
            'display',
            'show',
            'css',
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

    NORMAL_USER = _meta(
        full = 'normal_user',
        show = False,
        permission = []
    )

    NORMAL_ADMIN = _meta(
        full = 'normal_admin',
        show = True,
        css = 'ui red ribbon label',
        display = 'Admin',
        permission = ( _Permission.CONTEST_HIDE_SUBMISSION , _Permission.CONTEST_VIEW_ALL, _Permission.PROBLEM_ADD_PPROBLEM, _Permission.PROBLEM_CHANGE_PROBLEM , _Permission.PROBLEM_DOWNLOAD_DATA , _Permission.PROBLEM_VIEW_ALL , _Permission.SUBMISSION_VIEW_ALL )
    )

    SUPER_ADMIN = _meta(
        full = 'super_admin',
        show = True,
        css = 'ui green ribbon label',
        display = 'Super Admin',
        permission = NORMAL_ADMIN.permission + ( _Permission.CONTEST_ADD_CONTEST , _Permission.CONTEST_CHANGE_CONTEST , _Permission.USER_SET_NORMAL_ADMIN )
    )

    ROOT = _meta(
        full = 'root',
        show = True,
        css = 'ui orange ribbon label',
        display = 'Super Root',
        permission = tuple( _Permission )
    )

def get_user_group( full ):
    for each in Group:
        if each.value.full == full:
            return each
    return None

