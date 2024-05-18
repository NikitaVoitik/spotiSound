from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import RegisterSerializer, ProfileSerializer
from .permissions import IsOwner, IsOwnerOrReadOnly
from rest_framework.generics import CreateAPIView


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'User registered successfully'}, status=201)


class ProfileView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, pk):
        profile = get_object_or_404(Profile, user_id=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=400)
        return Response({'message': 'User logged out successfully'}, status=205)
