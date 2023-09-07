from asgiref.sync import async_to_sync
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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

    def validate(self, attrs):
        request = self.context.get('request')
        chat_id = request.user.chat_id
        if chat_id:
            attrs['author'] = request.user
            return attrs
        else:
            raise ValidationError('You have not bind a telegram chat yet')

    def create(self, validated_data):
        user = validated_data['author']
        message = (f"{user.name}, я получил от тебя сообщение:\n"
                   f"{validated_data['body']}")
        send_message(user.chat_id, message)
        return super().create(validated_data)
