from rest_framework import serializers
from user_account.models import User


class UserSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'company']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'role': {'required': True},
            'company': {'required': False},
        }
