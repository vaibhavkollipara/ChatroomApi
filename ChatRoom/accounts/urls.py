from django.conf.urls import url
from .views import (UserCreateApiView,
                    UserRetrieveApiView,
                    UserListApiView)

urlpatterns = [
    url(r'^signup/$', UserCreateApiView.as_view() , name="signup" ),
    url(r'^mydetails/$', UserRetrieveApiView.as_view(), name="mydetails"),
    url(r'^users/$', UserListApiView.as_view(), name="userslist"),
]
