from functools import wraps

import jwt
from django.http import Http404, JsonResponse
from rest_framework.exceptions import PermissionDenied


def error404(request, exception):
    raise Http404


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """

    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response

        return decorated

    return require_scope


def verify_user_type(request, expected_type, no_except=False):
    user_type = request.user.user_type()
    if user_type != expected_type:
        if no_except:
            return False
        raise PermissionDenied(detail=f'Wrong user type for resource. Expected: {expected_type}. Got: {user_type}')

    return True


def post_serialize(request, serializer_cls):
    serializer = serializer_cls(data=request.data)

    if serializer.is_valid(raise_exception=True):
        return serializer


def put_serialize(request, model_object, serializer_cls):
    serializer = serializer_cls(model_object, data=request.data)

    if serializer.is_valid(raise_exception=True):
        return serializer
