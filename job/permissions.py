from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.advertiser.user == request.user


class IsEmployer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.is_authenticated and request.user.employer
        except:
            return False


class IsEmployerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return request.user.is_authenticated and request.user.employer
        except:
            return False


class IsApplicant(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.is_authenticated and request.user.applicant
        except:
            return False
