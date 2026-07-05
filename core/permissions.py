from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'user', None) or getattr(getattr(obj, 'creator', None), 'user', None)
        return owner == request.user or request.user.is_staff


class IsCreator(permissions.BasePermission):
    message = 'A verified or pending creator profile is required.'

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and hasattr(request.user, 'creator_profile')
            and request.user.creator_profile.can_upload
        )


class IsVerifiedCreator(permissions.BasePermission):
    message = 'A verified creator profile is required.'

    def has_permission(self, request, view):
        profile = getattr(request.user, 'creator_profile', None)
        return bool(request.user and request.user.is_authenticated and profile and profile.is_verified)
