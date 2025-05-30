from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from users.models import ConfirmationCode



class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        code = data.get('code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')

        confirmation_code = ConfirmationCode.objects.filter(user=user).first()
        if not confirmation_code or confirmation_code.code != code:
            raise serializers.ValidationError('Invalid or expired confirmation code.')

        return data



class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


    def validate_username(self, username):
        try:
            User.objects.filter(username=username)
        except User.DoesNotExist:
            raise ValidationError('User already exists!')
        return username