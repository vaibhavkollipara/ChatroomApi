from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    Serializer
)
from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import ChatRoom, Message,ChatRoomMembership
from django.contrib.auth.models import User


class ChatRoomCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields =[
            'name',
            'admin'
        ]


class ChatRoomDeleteSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields =[
            'name',
            'slug'
        ]

class ChatRoomListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='chat:chatroommessages',
        lookup_field='slug'
    )
    
    class Meta:
        model = ChatRoom
        fields = [
            'name',
            'slug',
            'url',
            'date_created'
        ]


class ChatRoomMembershipCreateSerializer(Serializer):
    username = serializers.CharField()

    class Meta:
        model = ChatRoomMembership
        fields = [
            'chat_room',
            'username'
        ]

    def create(self, validated_data):
        chat_room = validated_data['chat_room']
        username = validated_data['username']
        try:
            user = User.objects.get(username=username)
        except:
            raise APIException("Invalid User")
        membership = ChatRoomMembership(chat_room=chat_room,user=user)
        try:
            membership.save()
        except:
            raise APIException("Seems like user is already a member")
        return validated_data


class MembershipDeleteSerializer(ModelSerializer):

    class Meta:
        model = ChatRoomMembership
        fields =[
            'chat_room',
            'user'
        ]



class ChatRoomMembersListSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'name',
            'email'
        ]

    def get_name(self,obj):
        return obj.get_full_name()


class MessageCreateSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'message'
        ]


class MessageListSerializer(ModelSerializer):
    sender = SerializerMethodField()

    class Meta:
        model = Message
        fields =[
            'message',
            'sender',
            'timestamp'
        ]

    def get_sender(self,obj):
        return str(obj.sender.get_full_name())