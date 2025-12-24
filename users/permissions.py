from rest_framework.permissions import BasePermission


class IsOwnerProfile(BasePermission):
    """
    Можно:
    - смотреть любой профиль
    - редактировать только свой
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET",):
            return True
        return obj == request.user
