from json import loads
from datetime import datetime

def Lutece_payload( user , context = None ):
    payload = {
        'username': user.username,
        'pk' : user.pk,
        'displayname' : user.display_name,
        'gravataremail' : user.gravataremail
    }
    return payload
