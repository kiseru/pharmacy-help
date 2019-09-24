from rest_framework import permissions


class IsApothecary(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'apothecary'


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'
