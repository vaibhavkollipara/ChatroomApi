from rest_framework.serializers import (
                    ModelSerializer,
                    SerializerMethodField
)
from rest_framework.exceptions import APIException
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        ]
        extra_kwargs = {
            "password":{
                "write_only" : True
            }
        }

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        user_obj = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username)
        user_obj.set_password(password)
        try:
            user_obj.save()
        except:
            raise APIException("Problem creating account !Try again with different details")
        return validated_data


class UserRetrieveSerializer(ModelSerializer):
    fullname = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'fullname',
            'username',
            'email'
        ]

    def get_fullname(self,obj):
        return obj.get_full_name()
