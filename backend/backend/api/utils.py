from django.contrib.auth import authenticate
from django.conf import settings

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
    jwks = requests.get(f"{settings.AUTH0_ISSUER}.well-known/jwks.json").json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = settings.AUTH0_ISSUER
    audience = settings.AUTH0_AUDIENCE
    return jwt.decode(token, public_key, audience=audience, issuer=issuer, algorithms=['RS256'])


def location(request, path):
    return '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host()) + path


def make_docx(bool_list, string_list):
    doc = docx.Document()
    para = doc.add_paragraph("")
    
    for i in range(len(string_list)):
        if i < len(bool_list) and bool_list[i] == True:
            para.add_run(string_list[i] + "").font.highlight_color = WD_COLOR_INDEX.GRAY_25
        else:
            para.add_run(string_list[i] + "")

    return True
