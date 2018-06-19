from enum import Enum, unique
from django.contrib.auth.models import Permission

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
    PROBLEM_VIEW_ALL = _meta(
        app_label = 'problem',
        model = 'problem',
        codename = 'view_all',)

@unique
class Group( Enum ):

    class _meta:
        __slots__ = (
            'full',
            'display',
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
    )

    NORMAL_ADMIN = _meta(
        full = 'normal_admin',
        display = 'Admin',
    )

    SUPER_ADMIN = _meta(
        full = 'super_admin',
        display = 'Super Admin',
    )