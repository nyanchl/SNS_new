from rest_framework import serializers
from app.models import MyText


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyText
        fields = ('user', 'text', 'textpoint','created_datetime')