from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from chats.models import Chat
from chats.permissions import ChatPermission
from chats.serializers import ChatSerializer


class ChatViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, ChatPermission)
    queryset = Chat.objects.all().select_related('group')
    serializer_class = ChatSerializer
    filterset_fields = ('group',)

    def get_queryset(self):
        return ChatPermission.scoped_queryset(self.request, self.queryset)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        chat: Chat = self.get_object()
        chat.add_like(request.user)
        return Response(status=status.HTTP_200_OK)

    @like.mapping.delete
    def remove_like(self, request, pk=None):
        chat: Chat = self.get_object()
        chat.remove_like(request.user)
        return Response(status=status.HTTP_200_OK)
