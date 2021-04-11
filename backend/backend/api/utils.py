from django.contrib.auth import authenticate

import json

import jwt
import requests


# These are here for Auth0 stuff
def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    # authenticate(remote_user=username)

    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('avpd.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('avpd.us.auth0.com')
    audience = 'https://api.avpd'
    # audience = 'https://avpd.us.auth0.com/auth/v2/'
    return jwt.decode(token, public_key, audience=audience, issuer=issuer, algorithms=['RS256'])


def location(request, path):
    return '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host()) + path
