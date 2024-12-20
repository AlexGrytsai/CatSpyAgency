from rest_framework.permissions import BasePermission
from django.core.exceptions import PermissionDenied


class IsAdminOrCatAssigned(BasePermission):
    """
    A custom permission class that checks if the requesting user is assigned
    to the object's cat.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if obj.cat and obj.cat.user == request.user:
            return True

        raise PermissionDenied(
            "You do not have permission to edit this mission."
        )
