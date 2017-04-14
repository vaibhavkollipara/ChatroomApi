from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
import datetime


class ChatRoom(models.Model):
    name = models.CharField(max_length=120)
    members = models.ManyToManyField(User, through='ChatRoomMembership')
    admin = models.ForeignKey(User,related_name='admin',default=1,blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,blank=True,default='')
    date_created = models.DateTimeField(auto_now_add=True,blank=True)

    def save(self,*args,**kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name)
            qs = ChatRoom.objects.filter(slug=self.slug).exists()
            if qs:
                now = datetime.datetime.now()
                self.slug = '{}-{}{}'.format(self.slug,now.minute,now.microsecond)
        super(ChatRoom,self).save(*args,**kwargs)
        membership = ChatRoomMembership(chat_room=self,user=self.admin)
        membership.save()

    def get_absolute_url(self):
        return reverse('chat:chatroommessages',kwargs={'slug' : self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering= ['-date_created']


class ChatRoomMembership(models.Model):
    chat_room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return "{} in {}".format(self.user.get_full_name(),self.chat_room.name)

    class Meta:
        unique_together = ['user','chat_room']
        order_with_respect_to = 'chat_room'


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-timestamp','sender']

