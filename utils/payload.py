from json import loads
from datetime import datetime

def Lutece_payload(user, context=None):
    return {
        'pk' : user.pk,
        'displayname' : user.display_name,
        'gravataremail' : user.gravataremail
    }