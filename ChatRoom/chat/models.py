from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
import datetime
from django.core.cache import cache
from .Cache import Cache, ChatroomCache
from rest_framework.exceptions import APIException


class ChatRoomManager(models.Manager):

    def get_chatrooms(self, user):
        myCache = cache.get("chatroom")
        chatrooms = None
        if not myCache:
            myCache = Cache()
        if user.id in myCache.users.keys():
            # if myCache.users[self.request.user.id]:
                # print("Chatrooms : Cache Hit")
            if not myCache.users[user.id]:
                myCache.users[user.id] = user.chatroom_set.all()
                cache.set("chatroom", myCache)
        else:
            # print("Cache miss")
            myCache.users[user.id] = user.chatroom_set.all()
            cache.set("chatroom", myCache)
        return myCache.users[user.id]

    def get_members(self, chat_room_slug):
        myCache = cache.get("chatroom")
        if not myCache:
            myCache = Cache()
        if chat_room_slug in myCache.chatrooms.keys():
            # if myCache.chatrooms[chat_room_slug].members:
                # print("Members : Cache Hit")
            if not myCache.chatrooms[chat_room_slug].members:
                myCache.chatrooms[chat_room_slug].members = ChatRoom.objects.get(slug=chat_room_slug).members
                cache.set("chatroom", myCache)
            return myCache.chatrooms[chat_room_slug].members
        else:
            chatroom = None
            try:
                chatroom = ChatRoom.objects.get(slug=chat_room_slug)
            except:
                raise APIException("Chatroom does not exist")
            chatroomCache = ChatroomCache()
            chatroomCache.members = chatroom.members.all()
            myCache.chatrooms[chat_room_slug] = chatroomCache
            cache.set("chatroom", myCache)
            return chatroomCache.members

    def get_messages(self, chat_room_slug):
        myCache = cache.get("chatroom")
        if not myCache:
            myCache = Cache()
        if chat_room_slug in myCache.chatrooms.keys():
            # if myCache.chatrooms[chat_room_slug].messages:
                # print("Messages : Cache Hit")
            if not myCache.chatrooms[chat_room_slug].messages:
                myCache.chatrooms[chat_room_slug].messages = ChatRoom.objects.get(slug=chat_room_slug).message_set.all()
                cache.set("chatroom", myCache)
            return myCache.chatrooms[chat_room_slug].messages
        else:
            chat_room = None
            try:
                chat_room = ChatRoom.objects.get(slug=chat_room_slug)
            except:
                raise APIException("Chatroom does not exist")
            chatroomCache = ChatroomCache()
            chatroomCache.messages = chat_room.message_set.all()
            myCache.chatrooms[chat_room_slug] = chatroomCache
            cache.set("chatroom", myCache)
            return chatroomCache.messages


class ChatRoom(models.Model):
    name = models.CharField(max_length=120)
    members = models.ManyToManyField(User, through='ChatRoomMembership')
    admin = models.ForeignKey(User, related_name='admin', default=1, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    objects = ChatRoomManager()

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name)
            qs = ChatRoom.objects.filter(slug=self.slug).exists()
            if qs:
                now = datetime.datetime.now()
                self.slug = '{}-{}{}'.format(self.slug, now.minute, now.microsecond)
        super(ChatRoom, self).save(*args, **kwargs)
        membership = ChatRoomMembership(chat_room=self, user=self.admin)
        membership.save()

    def get_absolute_url(self):
        return reverse('chat:chatroommessages', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']


class ChatRoomMembership(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{} in {}".format(self.user.get_full_name(), self.chat_room.name)

    class Meta:
        unique_together = ['user', 'chat_room']
        order_with_respect_to = 'chat_room'


class MessageManager(models.Manager):
    pass


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-timestamp', 'sender']
