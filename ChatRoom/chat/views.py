from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView
)
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ChatRoomCreateUpdateSerializer,
    ChatRoomListSerializer,
    ChatRoomDeleteSerializer,
    MessageListSerializer,
    MessageCreateSerializer,
    ChatRoomMembershipCreateSerializer,
    ChatRoomMembersListSerializer,
    MembershipDeleteSerializer
)
from rest_framework.exceptions import APIException
from .paginations import MyPageNumberPagination
from .permissions import (IsRoomMember,
                          IsRoomAdmin
                          )
from .models import (
    ChatRoom,
    ChatRoomMembership
)

from django.core.cache import cache
from .Cache import Cache, ChatroomCache


def index(request):
    return HttpResponse('<h1>Hello</h1>')


class ChatRoomCreateApiView(CreateAPIView):
    serializer_class = ChatRoomCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        admin = self.request.user
        serializer.save(admin=admin)


class ChatRoomUpdateApiView(RetrieveUpdateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsRoomMember]
    lookup_field = 'slug'


class ChatRoomListApiView(ListAPIView):
    serializer_class = ChatRoomListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return ChatRoom.objects.get_chatrooms(self.request.user)


class ChatRoomDeleteApiView(DestroyAPIView):
    serializer_class = ChatRoomDeleteSerializer
    permission_classes = [IsAuthenticated, IsRoomAdmin]
    lookup_url_kwarg = 'slug'

    def get_object(self):
        chatroom_slug = self.kwargs.get(self.lookup_url_kwarg)
        try:
            chat_room = ChatRoom.objects.get(slug=chatroom_slug)
        except:
            raise APIException("Invalid chatroom")
        return chat_room


class MembershipDeleteApiView(DestroyAPIView):
    serializer_class = MembershipDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'slug'

    def get_object(self):
        chatroom_slug = self.kwargs.get(self.lookup_url_kwarg)
        try:
            chat_room = ChatRoom.objects.get(slug=chatroom_slug)
        except:
            raise APIException("Invalid chatroom")
        user = self.request.user
        try:
            obj = ChatRoomMembership.objects.get(chat_room=chat_room, user=user)
        except:
            raise APIException("You are not a member to exit this room")
        return obj


class ChatRoomMembershipCreateApiView(CreateAPIView):
    serializer_class = ChatRoomMembershipCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'slug'

    def perform_create(self, serializer):
        chatroom_slug = self.kwargs.get(self.lookup_url_kwarg)
        try:
            chat_room = ChatRoom.objects.get(slug=chatroom_slug)
        except:
            raise APIException("Invalid Chatroom")
        serializer.save(chat_room=chat_room)


class MessageCreateApiView(CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [IsAuthenticated, IsRoomMember]
    lookup_url_kwarg = 'slug'

    def perform_create(self, serializer):
        chatroom_slug = self.kwargs.get(self.lookup_url_kwarg)
        self.check_object_permissions(self.request, chatroom_slug)
        try:
            chat_room = ChatRoom.objects.get(slug=chatroom_slug)
        except:
            raise APIException("Invalid Chatroom")
        serializer.save(chat_room=chat_room, sender=self.request.user)


class ChatRoomMembersListApiView(ListAPIView):
    serializer_class = ChatRoomMembersListSerializer
    permission_classes = [IsAuthenticated, IsRoomMember]
    lookup_url_kwarg = 'slug'

    def get_queryset(self, *args, **kwargs):
        chat_room_slug = self.kwargs.get(self.lookup_url_kwarg)
        self.check_object_permissions(self.request, chat_room_slug)
        return ChatRoom.objects.get_members(chat_room_slug)


class MessageListApiView(ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [IsAuthenticated, IsRoomMember]
    lookup_url_kwarg = 'slug'
    pagination_class = MyPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        chat_room_slug = self.kwargs.get(self.lookup_url_kwarg)
        self.check_object_permissions(self.request, chat_room_slug)
        return ChatRoom.objects.get_messages(chat_room_slug)
