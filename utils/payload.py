from json import loads
from datetime import datetime
from graphql_jwt.utils import jwt_payload


def Lutece_payload(user, context=None):
    payload = jwt_payload(user)
    payload['displayname'] = user.display_name
    payload['gravataremail'] = user.gravataremail
    return payload
