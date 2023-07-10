from django.contrib.auth import get_user_model

from rest_framework import viewsets,generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header

from .serializers import UserSerializer,TextSerializer,LoginedSerializer
from accounts.models import AuthUser
from app.models import MyText


class UserApiSet(viewsets.ModelViewSet):
    queryset = MyText.objects.all()
    serializer_class = TextSerializer

    def get_queryset(self):
        queryset = MyText.objects.all()
        return queryset
    
    def get_logined_user(self, request):
        queryset = AuthUser.objects.filter(username=request.user)
        serializer = LoginedSerializer(queryset)
        return serializer


class UserViewSet(viewsets.ModelViewSet):
    """ユーザー情報"""
    
    queryset = AuthUser.objects.filter(username="Nyanchl")
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)