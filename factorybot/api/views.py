from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, generics, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.models import User, Message
from api.schema import UserLoginSerializer, StatusTrueSerializer
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
        Register user
        """
        # required_fields = {'username', 'password', 'name'}
        # absent_required_fields = required_fields.difference(request.data)
        # if absent_required_fields:
        #     return JsonResponse(
        #         {
        #             'Errors': f"Не указаны необходимые аргументы: "
        #                       f"{', '.join(absent_required_fields)}"
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # TODO move validation to serializer
        try:
            validate_password(request.data['password'])
        except ValidationError as password_error:
            return JsonResponse(
                {'Errors': {'password': list(password_error)}},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
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

    # TODO authorization via my endpoint?
    @extend_schema(
        request=UserLoginSerializer,
        responses={200: StatusTrueSerializer}
    )
    @action(methods=['post'], detail=False)
    def login(self, request):
        """
        User authorization
        """
        if not {'username', 'password'}.issubset(request.data):
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Не указаны все необходимые аргументы'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            username=request.data['username'],
            password=request.data['password']
        )

        if user is not None:
            return JsonResponse({'Status': True})
        else:
            return JsonResponse(
                {'Errors': 'Не удалось авторизовать'},
                status=status.HTTP_400_BAD_REQUEST
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
