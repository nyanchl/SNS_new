from rest_framework import serializers
from app.models import MyText


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyText
        fields = ('id','user', 'text', 'textpoint','created_datetime')

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyText
        fields = ('text','textpoint')