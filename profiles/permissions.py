from rest_framework.permissions import BasePermission


class IsCandidate(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "CANDIDATE"
        )


class IsEmployer(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "EMPLOYER"
        )


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        # Admin can access everything
        if request.user and request.user.is_staff:
            return True

        # Only owner can access their own profile
        return obj.user == request.user