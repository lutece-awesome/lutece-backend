from enum import Enum, unique
from utils.decorators import classproperty

class _meta:
    __slots__ = (
        'full',
        'version',
        'codemirror',
        'info',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = [x for x in kw]

    def __str__(self):
        return f'<Language:{ self.full }>'

    def __repr__(self):
        return f'<Language:{ self.full }>'
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }
        
@unique
class Language( Enum ):
            
    _GNUCPP = _meta(
        full = 'GNU G++',
        version = '7.3.0',
        info = 'GNU G++17',
        codemirror = 'text/x-c++src',
    )

    _GNUGCC = _meta(
        full = 'GNU GCC',
        version = '7.3.0',
        info = 'GNU GCC 7.3',
        codemirror = 'text/x-csrc',
    )

    _CLANG = _meta(
        full = 'Clang',
        version = '6.0.0',
        info = 'Clang 6.0.0',
        codemirror = 'text/x-c++src',
    )

    _PYTHON = _meta(
        full = 'Python',
        version = '3.6.5',
        info = 'Python 3.6.5',
        codemirror = 'text/x-python'
    )

    _JAVA = _meta(
        full = 'Java',
        version = '10',
        info = 'Java 10',
        codemirror = 'text/x-java'
    )

    _GO = _meta(
        full = 'Go',
        version = '1.10.2',
        info = 'Go 1.10.2',
        codemirror = 'text/x-go'
    )

    _RUBY = _meta(
        full = 'Ruby',
        version = '2.5.1',
        info = 'Ruby 2.5.1',
        codemirror = 'text/x-ruby'
    )

    _RUST = _meta(
        full = 'Rust',
        version = '1.26.1',
        info = 'Rust 1.26.1',
        codemirror = 'text/x-rustsrc'
    )

    @classproperty
    def GNUCPP( cls ):
        return cls._GNUCPP.value

    @classproperty
    def GNUGCC( cls ):
        return cls._GNUGCC.value
    
    @classproperty
    def CLANG( cls ):
        return cls._CLANG.value

    @classproperty
    def PYTHON( cls ):
        return cls._PYTHON.value

    @classproperty
    def JAVA( cls ):
        return cls._JAVA.value
    
    @classproperty
    def GO( cls ):
        return cls._GO.value

    @classproperty
    def RUBY( cls ):
        return cls._RUBY.value

    @classproperty
    def RUST( cls ):
        return cls._RUST.value

    @classmethod
    def value_of( cls , value ):
        for each in cls:
            if each.value.full == value:
                return each.value
        return None

    @classmethod
    def all( cls ):
        return [ each.value for each in cls ]
