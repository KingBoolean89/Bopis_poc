from rest_framework.permissions import BasePermission
from common.utils import authenticate

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = authenticate(self, request)
        return bool(request.user and user)