import secrets

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.models import User, Message
from api.serializers import UserSerializer, MessageSerializer


class UserViewSet(viewsets.GenericViewSet):
    """
    User viewset
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = []

    # @extend_schema(request=UserRegisterSerializer)
    @action(methods=['post'], detail=False)
    def register(self, request):
        """
        Регистрация пользователя
        """
        user_serializer = self.get_serializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return JsonResponse(
                self.get_serializer(user).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse(
                {'Errors': user_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='token')
    def get_token(self, request):
        """
        Получение токена для привязки чата Telegram
        """
        user = request.user
        if user.token:
            token = user.token
        else:
            token = secrets.token_hex(10)
            user.token = token
            user.save()
        return JsonResponse({'token': token})


@extend_schema_view(
    list=extend_schema(description='Получение списка сообщений, отправленных '
                                   'текущим пользователем'),
    create=extend_schema(description='Отправка сообщения в чат Telegram'),
)
class MessageViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    Message viewset
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return Message.objects.filter(author=current_user)
