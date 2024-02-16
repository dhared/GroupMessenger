from rest_framework.permissions import BasePermission


class GroupPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()

    @classmethod
    def scoped_queryset(cls, request, queryset):
        return queryset.filter(members=request.user)
