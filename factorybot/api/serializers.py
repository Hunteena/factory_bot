from asgiref.sync import async_to_sync
from django.conf import settings
from rest_framework import serializers
from telegram import Bot

from api.models import Message, User


# @extend_schema_serializer(exclude_fields=['address'])
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name']


@async_to_sync
async def send_message(chat_id, body):
    bot = Bot(settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=body)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        send_message(1587425426, validated_data['body'])
        return super().create(validated_data)
