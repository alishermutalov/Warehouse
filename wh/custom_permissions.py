from rest_framework import permissions
from users.models import MANAGER, ADMIN


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allowed any request for GET (read-only) methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #Allowed PUT, POST, PATCH, DELETE for admins and managers 
        return request.user and request.user.role in [MANAGER, ADMIN]
