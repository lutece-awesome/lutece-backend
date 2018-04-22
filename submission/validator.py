from django.conf import settings

def validate_fetch_judge( request ):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']
    if ip not in settings.JUDGE_VALID_IPPOOL:
        return False
    return True