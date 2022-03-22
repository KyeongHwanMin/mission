from django.contrib.auth import get_user_model
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated:
            if obj.__class__ == get_user_model():
                return obj == request.user
            return False
        else:
            return False



