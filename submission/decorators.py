from .validator import validate_fetch_judge

def validator_fetch_judge( function ):
    def wrapper( * argv , ** kw ):
        try:
            if validate_fetch_judge( argv[0] ) == False:
                raise PermissionError()
        except PermissionError:
            raise Http404( 'Permission Denied' )
        except:
            raise Http404( 'Unknown Error' )
        return function( * argv , ** kw )
    return wrapper