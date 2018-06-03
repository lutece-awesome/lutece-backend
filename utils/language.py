from enum import Enum, unique

class _meta:
    __slots__ = (
        'full',
        'version',
        'prism',
        'codemirror',
        'info',
        '_field'
    )

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
class Language( Enum ):
    GNUCPP = _meta(
        full = 'GNU G++',
        version = '7.3.0',
        prism = 'language-cpp',
        info = 'GNU G++17',
        codemirror = 'text/x-c++src',
    )
    GNUGCC = _meta(
        full = 'GNU GCC',
        version = '7.3.0',
        prism = 'language-c',
        info = 'GNU GCC 7.3',
        codemirror = 'text/x-csrc',
    )
    CLANG = _meta(
        full = 'Clang',
        version = '6.0.0',
        prism = 'language-cpp',
        info = 'Clang 6.0.0',
        codemirror = 'text/x-c++src',
    )
    PYTHON = _meta(
        full = 'Python',
        version = '3.6.5',
        prism = 'language-python',
        info = 'Python 3.6.5',
        codemirror = 'text/x-python'
    )
    JAVA = _meta(
        full = 'Java',
        version = '10',
        prism = 'language-java',
        info = 'Java 10',
        codemirror = 'text/x-java'
    )
    GO = _meta(
        full = 'Go',
        version = '1.10.2',
        prism = 'language-go',
        info = 'Go 1.10.2',
        codemirror = 'text/x-go'
    )
    RUBY = _meta(
        full = 'Ruby',
        version = '2.5.1',
        prism = 'language-ruby',
        info = 'Ruby 2.5.1',
        codemirror = 'text/x-ruby'
    )
    RUST = _meta(
        full = 'Rust',
        version = '1.26.1',
        prism = 'language-rust',
        info = 'Rust 1.26.1',
        codemirror = 'text/x-rustsrc'
    )


def get_language( result ):
    for each in Language:
        if each.value.full == result:
            return each
    return None

def get_prism( result ):
    return get_language( result ).value.prism

def get_language_list():
    return list( Language )