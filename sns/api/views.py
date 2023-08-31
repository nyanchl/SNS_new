from rest_framework import viewsets,filters
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer,TextSerializer
from accounts.models import AuthUser
from app.models import MyText


class UserApiSet(viewsets.ModelViewSet):
    queryset = MyText.objects.all()
    serializer_class = TextSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('uuid')


class LoginedUserSet(viewsets.ModelViewSet):
    """ユーザー情報"""
    
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)