from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer, UserConfirmSerializer, UserLoginSerializer
from .models import User

@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пользователь создан. Проверьте email для кода подтверждения.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_user(request):
    serializer = UserConfirmSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('username')  # username теперь email
        code = serializer.validated_data['code']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
        if user.confirmation_code == code:
            user.is_active = True
            user.confirmation_code = None
            user.save()
            return Response({'message': 'Пользователь подтверждён.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверный код.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            return Response({'message': 'Авторизация успешна.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Неверные данные или пользователь не подтверждён.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
