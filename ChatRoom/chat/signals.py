from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import ChatRoom, ChatRoomMembership


@receiver(post_save, sender=ChatRoomMembership)
@receiver(post_delete, sender=ChatRoomMembership)
def modified_Membership(sender, instance, ** kwargs):
    print("Modified Membership : Cache Update")
    myCache = cache.get("chatroom")
    myCache.users[instance.user.id] = instance.user.chatroom_set.all()
    myCache.chatrooms[instance.chat_room.slug] = instance.chat_room.members.all()
    cache.set("chatroom", myCache)
