from django.conf import settings
from django.http import HttpResponse

AUTH_KEY = settings.DATA_SERVER.get('auth_key')


def judger_auth(function):
    def wrapper(*argv, **kw):
        try:
            print( argv[0].POST.get('authkey').encode('ascii'), AUTH_KEY)
            if argv[0].POST.get('authkey').encode('ascii') != AUTH_KEY:
                print( 'not equal' )
                return HttpResponse(None)
        except Exception as e:
            return HttpResponse(None)
        return function(*argv, **kw)

    return wrapper
