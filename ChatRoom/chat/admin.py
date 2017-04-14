from django.contrib import admin
from .models import (
    ChatRoom,
    ChatRoomMembership,
    Message
)


class ChatRoomAdminModel(admin.ModelAdmin):
    list_filter = ['name', 'date_created']
    list_display = ['name', 'slug', 'date_created']


class ChatRoomMembershipAdminModel(admin.ModelAdmin):
    list_display = ['user', 'chat_room','date_joined']
    list_filter = ['chat_room','user']


class MessageAdminMode(admin.ModelAdmin):
    list_display = ['message','sender','chat_room', 'timestamp']
    list_filter = ['sender', 'chat_room', 'timestamp']

admin.site.register(ChatRoom, ChatRoomAdminModel)
admin.site.register(ChatRoomMembership,ChatRoomMembershipAdminModel)
admin.site.register(Message,MessageAdminMode)
