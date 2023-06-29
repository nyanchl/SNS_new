from rest_framework import viewsets,generics
from accounts.models import AuthUser
from app.models import MyText
from .serializers import UserSerializer,TextSerializer
from rest_framework.permissions import IsAuthenticated


class UserApiSet(viewsets.ModelViewSet):
    queryset = MyText.objects.all()
    serializer_class = TextSerializer

    def get_queryset(self):
        queryset = MyText.objects.all()
        L_id = self.request.query_params.get('id')

        if L_id:
            queryset = queryset.filter(user_id=L_id)
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    #ユーザー情報
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)