from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def get_role(user):
    if user.doctor:
        role = 'doctor'
    elif user.apothecary_set.count():
        role = 'apothecary'
    else:
        raise Exception('No such role')
    return role


class AdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_admin
