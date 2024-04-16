from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .utils import generate_access_token, generate_refresh_token


@api_view(['POST'])
def user_registration(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if email and password:
        try:
            CustomUser.objects.get(email=email)
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user = CustomUser.objects.create_user(email=email, password=password)
            return Response({"id": user.id, "email": user.email}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "НBoth email and password are required."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        return Response({"access_token": access_token, "refresh_token": refresh_token})
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def token_refresh(request):
    refresh_token = request.data.get('refresh_token')
    if refresh_token:
        user_id = CustomUser.objects.filter(refresh_token=refresh_token).values_list('id', flat=True).first()
        if user_id:
            user = CustomUser.objects.get(id=user_id)
            access_token = generate_access_token(user)
            new_refresh_token = generate_refresh_token(user)
            return Response({"access_token": access_token, "refresh_token": new_refresh_token})
    return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    user = request.user
    user.refresh_token = None
    user.save()
    logout(request)
    return Response({"success": "User logged out."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({"id": user.id, "email": user.email})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    user = request.user
    new_email = request.data.get('email')
    if new_email:
        user.email = new_email
        user.save()
        return Response({"id": user.id, "email": user.email})
    return Response({"error": "You must specify a new email address."}, status=status.HTTP_400_BAD_REQUEST)
