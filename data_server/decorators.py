from django.http import HttpResponse
from Lutece.settings import JUDGE_AUTH_KEY

def judger_auth( function ):
    def wrapper( * argv , ** kw ):
        try:
            if argv[0].POST.get( 'authkey' ) != JUDGE_AUTH_KEY:
                return HttpResponse( None )
        except:
            return HttpResponse( None )
        return function( * argv , ** kw )
    return wrapper
