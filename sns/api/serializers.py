from rest_framework import serializers
from app.models import MyText
from accounts.models import AuthUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyText
        fields = '__all__'