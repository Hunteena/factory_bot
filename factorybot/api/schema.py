from rest_framework import serializers

from api.models import User


# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'name']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class StatusTrueSerializer(serializers.Serializer):
    Status = serializers.BooleanField()
