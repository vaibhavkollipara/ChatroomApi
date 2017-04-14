from rest_framework.generics import (CreateAPIView,
                                     RetrieveAPIView,
                                     ListAPIView)
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import (UserCreateSerializer,
                          UserRetrieveSerializer)
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .paginations import MyPageNumberPagination
from django.contrib.auth.models import User


class UserCreateApiView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [ AllowAny ]

    def perform_create(self, serializer):
        serializer.save()


class UserRetrieveApiView(RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserListApiView(ListAPIView):
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name','last_name','username','email']


