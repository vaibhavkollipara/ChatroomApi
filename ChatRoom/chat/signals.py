from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import ChatRoom, ChatRoomMembership, Message
from .Cache import Cache, ChatroomCache


@receiver(post_save, sender=ChatRoomMembership)
@receiver(post_delete, sender=ChatRoomMembership)
def modified_Membership(sender, instance, ** kwargs):
    print("Modified Membership : Cache Update")
    myCache = cache.get("chatroom")
    if not myCache:
        myCache = Cache()
    if instance.user.id in myCache.users.keys():
        myCache.users[instance.user.id] = instance.user.chatroom_set.all()
    if instance.chat_room.slug not in myCache.chatrooms.keys():
        myCache.chatrooms[instance.chat_room.slug] = ChatroomCache()
    myCache.chatrooms[instance.chat_room.slug].members = instance.chat_room.members.all()
    cache.set("chatroom", myCache)


@receiver(post_save, sender=Message)
def new_message(sender, instance, **kwargs):
    print("New Message : Cache Update")
    myCache = cache.get("chatroom")
    if not myCache:
        myCache = Cache()
    if instance.chat_room.slug not in myCache.chatrooms.keys():
        myCache.chatrooms[instance.chat_room.slug] = ChatroomCache()
    myCache.chatrooms[instance.chat_room.slug].messages = instance.chat_room.message_set.all()
    cache.set("chatroom", myCache)
