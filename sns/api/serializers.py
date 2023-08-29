from rest_framework import serializers
from app.models import MyText
from accounts.models import AuthUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = 'uuid','username','name'


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyText
        fields = '__all__'