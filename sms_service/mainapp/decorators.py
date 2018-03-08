import base64

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from functools import wraps

def view_or_basicauth(view, obj, request, *args, **kwargs):
    # Check for valid basic auth header
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).decode("utf-8").split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None and user.is_active:
                    request.user = user
                    return view(obj, request, *args, **kwargs)

    # Either they did not provide an authorization header or
    # something in the authorization attempt failed. Send a 403
    # back to them to ask them to authenticate.
    response = HttpResponse()
    response.status_code = 403
    return response

def basicauth(view_func):
    def wrapper(obj, request, *args, **kwargs):
        return view_or_basicauth(view_func, obj, request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper