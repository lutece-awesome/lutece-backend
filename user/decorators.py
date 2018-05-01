from django.http import HttpResponse


def login_required_ajax( function ):
    def wrapper( * argv , ** kw ):
        try:
            if argv[0].user.is_authenticated == False:
                return HttpResponse( dumps( { 'error_msg' : 'Please log in first.' } ) , content_type = 'application/json' )
        except:
            return HttpResponse(dumps({'error_msg': 'Unknown error.'}), content_type='application/json')
        return function( * argv , ** kw )
    return wrapper
