from graphql_jwt.utils import jwt_payload


def payload_handler(user, context=None):
    payload = jwt_payload(user)
    payload['password'] = user.password[-8:]
    return payload
