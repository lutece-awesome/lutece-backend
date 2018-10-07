from pickle import dumps as pickle_dumps
from django.http import HttpResponse
from data.decorators import judger_auth
from data.util import process

@judger_auth
def fetch_data( request ):
    return HttpResponse( pickle_dumps( process( request ) , 2 ) , content_type = 'application/json' )