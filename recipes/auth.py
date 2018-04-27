from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def get_role(user):
    if user.doctor_set.count():
        role = 'doctor'
    elif user.apothecary_set.count():
        role = 'apothecary'
    else:
        role = 'admin'
    return role


def get_default_url(role):
    if role == 'doctor':
        return '/doctor'
    elif role == 'apothecary':
        return '/apothecary'
    else:
        return '/admin'


def login_not_required(url=None):
    def wrapper(func):
        def new_func(request, *args, **kwargs):
            get_token(request)
            if request.user.is_authenticated:
                new_url = url
                if not new_url:
                    new_url = get_default_url(get_role(request.user))
                return HttpResponseRedirect(new_url)
            else:
                return func(request, *args, **kwargs)

        return new_func
    return wrapper


def has_role(role, redirect_url=None):
    def wrapper(func):
        def new_func(request, *args, **kwargs):
            actual_role = get_role(request.user)
            if actual_role != role:
                # new_url = redirect_url
                # if not new_url:
                #     new_url = get_default_url(actual_role)
                # return HttpResponseRedirect(new_url)
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return func(request, *args, **kwargs)

        return new_func
    return wrapper


class ApothecaryPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return get_role(request.user) is 'apothecary'


class DoctorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return get_role(request.user) is 'doctor'
