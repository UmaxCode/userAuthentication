from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import (UserSignUpSerializer, UserLoginSerializer, TokenLoginSerializer)
from rest_framework import status
from rest_framework.authtoken.models import Token
from .utils import is_user_active, send_email_to_user
from .models import CustomUser


@api_view(['POST'])
def user_signup(request):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
        con_password = serializer.validated_data.get('con_password')
        password = serializer.validated_data.get('password')

        if password == con_password:
            user = serializer.save()
            user_token = Token.objects.get(user=user)
            user.is_active = False
            user.save()
            send_email_to_user(user.email, user_token.key)
            data = {'message': f'A user {user.username} is created successfully. \
              Check your mail for the verification token', 'token': user_token.key}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            error = {'error': 'passwords does not match'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login_up(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = CustomUser.objects.get(username=username)  # to get the email address of the user

        if not is_user_active(username):
            error = {'error': f'user {username} has not been verified. Check your email \
        {user.email} for the verification token.'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_token = Token.objects.get(user=user)
            data = {'message': f'A user {user.username} is logged in successfully', 'token': user_token.key}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            error = {'error': 'username or password does not match'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login_ut(request):
    serializer = TokenLoginSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        username = serializer.validated_data.get("username")
        token = serializer.validated_data.get("token")
        user = authenticate(request, username=username, token=token)
        if user is not None:
            user_token = Token.objects.get(user=user)
            data = {'message': f'A user {user.username} is logged in successfully', 'token': user_token.key}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            error = {'error': 'username or token does not match'}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

