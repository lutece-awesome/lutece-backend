from pickle import dumps as pickle_dumps
from django.http import HttpResponse
from .decorators import judger_auth
from .util import process
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@judger_auth
def fetch_data( request ):
    return HttpResponse( pickle_dumps( process( request ) ) , content_type = 'application/json' )