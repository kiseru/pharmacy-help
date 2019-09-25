from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsApothecary(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'apothecary'


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user.role == 'doctor'


class IsApothecaryOrIsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return
