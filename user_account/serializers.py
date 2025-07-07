from rest_framework import serializers
from user_account.models import User
from company.serializers import CompanySerializer


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'company']
