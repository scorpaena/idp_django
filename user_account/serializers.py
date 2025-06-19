from rest_framework import serializers
from user_account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'role': {'required': True}
        }
