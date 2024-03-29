from rest_framework import permissions


class IsAuthenticatedAndOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class HasExpiringLinks(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.account.has_expiring_links


class HasToken(permissions.BasePermission):

    def has_permission(self, request, view):
        return hasattr(request, 'token')
