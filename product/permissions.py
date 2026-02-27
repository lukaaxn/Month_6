from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    """
    Разрешение для модераторов (is_staff=True):
    - Может просматривать, изменять и удалять чужие продукты.
    - Не может создавать продукты (POST запрещён).
    """
    def has_permission(self, request, view):
        # Только модераторы
        if not request.user or not request.user.is_authenticated:
            return False
        if not request.user.is_staff:
            return False
        # POST запрещён
        if request.method == 'POST':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Модератор может просматривать, изменять и удалять чужие продукты
        if not request.user.is_staff:
            return False
        if request.method == 'POST':
            return False
        return True
