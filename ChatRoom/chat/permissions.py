from django.core.cache import cache
from .models import ChatRoom
from .Cache import Cache, ChatroomCache
from rest_framework.permissions import BasePermission


class IsRoomMember(BasePermission):
    message = "You must be member of this Chatroom to access this"

    def has_object_permission(self, request, view, chatroom_slug):
        myCache = cache.get("chatroom")
        if not myCache:
            myCache = Cache()

        if chatroom_slug in myCache.chatrooms.keys():
            if not myCache.chatrooms[chatroom_slug].members:
                myCache.chatrooms[chatroom_slug].members = ChatRoom.objects.get(slug=chatroom_slug).members.all()
                cache.set("chatroom", myCache)
            return request.user in myCache.chatrooms[chatroom_slug].members
        else:
            chatroom = None
            try:
                chatroom = ChatRoom.objects.get(slug=chatroom_slug)
            except:
                raise APIException("Invalid Chatroom")
            chatroomCache = ChatroomCache()
            chatroomCache.members = chatroom.members.all()
            myCache.chatrooms[chatroom_slug] = chatroomCache
            return request.user in chatroomCache.members


class IsRoomAdmin(BasePermission):
    message = "You must be Admin of this Chatroom to access this"

    def has_object_permission(self, request, view, obj):
        return request.user is obj.admin
