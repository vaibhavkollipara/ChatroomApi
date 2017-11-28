from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import (obtain_jwt_token,
                                      verify_jwt_token,
                                      refresh_jwt_token
                                      )

urlpatterns = [
    url(r'^auth/obtaintoken/$', obtain_jwt_token),
    url(r'^auth/verifytoken/$', verify_jwt_token),
    url(r'^auth/refreshtoken/$', refresh_jwt_token),
    url(r'^', include('chat.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
]
