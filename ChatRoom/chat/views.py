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
from .Cache import Cache


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
        myCache = cache.get("chatroom")
        chatrooms = None
        if not myCache:
            myCache = Cache()
            print("Cache Created")
        if self.request.user.id in myCache.users.keys():
            chatrooms = myCache.users[self.request.user.id]
            print("Cache hit")
        else:
            print("Cache miss")
            chatrooms = self.request.user.chatroom_set.all()
            myCache.users[self.request.user.id] = chatrooms
            cache.set("chatroom", myCache)
        return chatrooms


class ChatRoomDeleteApiView(DestroyAPIView):
    serializer_class = ChatRoomDeleteSerializer
    permission_classes = [IsAuthenticated, IsRoomAdmin]
    queryset = ChatRoom.objects.all()
    lookup_field = 'slug'


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
        try:
            chat_room = ChatRoom.objects.get(slug=chatroom_slug)
        except:
            raise APIException("Invalid Chatroom")
        user = self.request.user
        if user not in chat_room.members.all():
            raise APIException("You must be member of this chatroom for access")
        serializer.save(chat_room=chat_room, sender=user)


class ChatRoomMembersListApiView(ListAPIView):
    serializer_class = ChatRoomMembersListSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'slug'

    def get_queryset(self, *args, **kwargs):
        chat_room_slug = self.kwargs.get(self.lookup_url_kwarg)
        myCache = cache.get("chatroom")
        members = None
        if chat_room_slug in myCache.chatrooms.keys():
            print("Chatroom Members : Cache Hit")
            members = myCache.chatrooms[chat_room_slug]
        else:
            print("Chatroom Members : Cache Miss")
            try:
                chat_room = ChatRoom.objects.get(slug=chat_room_slug)
            except:
                raise APIException("Chatroom does not exist")
            members = chat_room.members.all()
            myCache.chatrooms[chat_room.slug] = members
            cache.set("chatroom", myCache)
        if self.request.user not in members:
            raise APIException("Must be member of this Chatroom to access")
        return members


class MessageListApiView(ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [IsAuthenticated, IsRoomMember]
    lookup_url_kwarg = 'slug'
    pagination_class = MyPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        chat_room_slug = self.kwargs.get(self.lookup_url_kwarg)
        try:
            chat_room = ChatRoom.objects.get(slug=chat_room_slug)
        except:
            raise APIException("Chatroom does not exist")
        if self.request.user not in chat_room.members.all():
            raise APIException("You must be member of this chatroom for access")
        qs = chat_room.message_set.all()
        return qs
