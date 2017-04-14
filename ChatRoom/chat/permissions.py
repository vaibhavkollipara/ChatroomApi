from rest_framework.permissions import BasePermission


class IsRoomMember(BasePermission):
    message = "You must be member of this Chatroom to access this"

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsRoomAdmin(BasePermission):
    message = "You must be Admin of this Chatroom to access this"

    def has_object_permission(self, request, view, obj):
        return request.user is obj.admin