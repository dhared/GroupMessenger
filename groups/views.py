from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from groups.models import Group
from groups.permissions import GroupPermission
from groups.serializers import GroupSerializer, UserIdSerializer


class GroupViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, GroupPermission)
    queryset = Group.objects.all().prefetch_related('members')
    serializer_class = GroupSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return GroupPermission.scoped_queryset(self.request, self.queryset)

    @action(methods=['POST'], detail=True)
    def member(self, request, pk=None):
        group = self.get_object()
        user_serializer = UserIdSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        group.add_members(user_serializer.validated_data['users'])
        group_serializer = GroupSerializer(instance=group)
        return Response(data=group_serializer.data, status=status.HTTP_200_OK)

    @member.mapping.delete
    def remove_member(self, request, pk=None):
        group = self.get_object()
        user_serializer = UserIdSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        group.remove_members(user_serializer.validated_data['users'])
        group_serializer = GroupSerializer(instance=group)
        return Response(data=group_serializer.data, status=status.HTTP_200_OK)
