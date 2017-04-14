from django.conf.urls import url
from .views import (index,
                    ChatRoomCreateApiView,
                    MessageListApiView,
                    ChatRoomMembershipCreateApiView,
                    MessageCreateApiView,
                    ChatRoomListApiView,
                    ChatRoomDeleteApiView,
                    ChatRoomUpdateApiView,
                    ChatRoomMembersListApiView,
                    MembershipDeleteApiView)

app_name="chat"

urlpatterns = [
    url(r'^$', index , name='home'),
    url(r'newchatroom/$', ChatRoomCreateApiView.as_view(), name='newchatroom'),
    url(r'deletechatroom/(?P<slug>[\w-]+)/$', ChatRoomDeleteApiView.as_view(), name='deletechatroom'),
    url(r'renamechatroom/(?P<slug>[\w-]+)/$', ChatRoomUpdateApiView.as_view(), name='renamechatroom'),
    url(r'mychatrooms/$',ChatRoomListApiView.as_view() , name='chatroomslist'),
    url(r'chatroom/(?P<slug>[\w-]+)/memberslist/$', ChatRoomMembersListApiView.as_view(), name="chatroomembers"),
    url(r'chatroom/(?P<slug>[\w-]+)/$', MessageListApiView.as_view(), name="chatroommessages"),
    url(r'chatroom/(?P<slug>[\w-]+)/newmember/$', ChatRoomMembershipCreateApiView.as_view(), name="newmembership"),
    url(r'chatroom/(?P<slug>[\w-]+)/exit/$', MembershipDeleteApiView.as_view(), name="deletemembership"),
    url(r'chatroom/(?P<slug>[\w-]+)/newmessage/$', MessageCreateApiView.as_view(), name="newmessage")
]
