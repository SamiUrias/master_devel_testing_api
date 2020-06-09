import hashlib
import hmac

from ..models import Credentials

X_ROUTE_REPRESENTATIONS = [
    '/message/',
    '/message/<id>/',
    '/message/<tag>/'
]


def is_valid_x_signature(x_signature, http_x_route, http_x_key, data=None):
    qs = Credentials.objects.filter(key=http_x_key).values_list(
        'shared_secret', flat=True)

    shared_secret = qs[0]

    print('Found shared_secret::', shared_secret)
    signature = signature_generator(http_x_route, shared_secret, data)

    print("A::", x_signature)
    print("B::", signature)

    return x_signature == signature


def authenticate(request_meta, request_data):
    print("Inside authenticate")
    # Get the 'X-KEY', 'X-Route' and 'X-Signature' headers
    http_x_key = request_meta.get('HTTP_X_KEY', None)
    http_x_route = request_meta.get('HTTP_X_ROUTE', None)
    http_x_signature = request_meta.get('HTTP_X_SIGNATURE', None)

    print("----")
    print("Here: ", http_x_key, http_x_route, http_x_signature)
    print("----")

    # Validate X-key
    # The x-key should exists in the database
    if http_x_signature is None:
        return False

    if not Credentials.objects.filter(key=http_x_key).exists():
        return False

    # Validate x-route
    # The x-route must exist and should contain a string representing the
    # route for the request
    if http_x_route is None:
        return False

    if http_x_route not in X_ROUTE_REPRESENTATIONS:
        return False

    # Validate x-signature
    if http_x_signature is None:
        return False

    if not is_valid_x_signature(http_x_signature,
                                http_x_route,
                                http_x_key,
                                request_data):

        print("=> Not valid signature")
        return False
    else:
        print("=> valid signature")

    return True


def signature_generator(http_x_route, shared_secret, data=None):
    body_tuple = data
    if not isinstance(data, dict):
        body_tuple = {}

    # ------------------------------------
    # Getting the body / url parameters and x-route
    # ------------------------------------
    lex_list = [body_tuple.keys(), body_tuple.values(), http_x_route]

    # Convert all the list elements into string
    lex_list = [str(element) for element in lex_list]

    pre_signed_data = ";".join(lex_list)

    # ------------------------------------
    # Create the HMAC-SHA256 signature
    # ------------------------------------
    signature = hmac.new(
        key=bytes(shared_secret, 'latin-1'),
        msg=bytes(pre_signed_data, 'latin-1'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return signature
