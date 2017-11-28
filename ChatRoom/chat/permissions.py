from django.core.cache import cache
from .models import ChatRoom
from .Cache import Cache, ChatroomCache
from rest_framework.permissions import BasePermission


class IsRoomMember(BasePermission):
    message = "You must be member of this Chatroom to access this"

    def has_object_permission(self, request, view, chatroom_slug):
        return ChatRoom.objects.get_members(chatroom_slug).filter(id=request.user.id).exists()


class IsRoomAdmin(BasePermission):
    message = "You must be Admin of this Chatroom to access this"

    def has_object_permission(self, request, view, obj):
        return request.user is obj.admin
