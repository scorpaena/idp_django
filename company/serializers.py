from rest_framework.serializers import ModelSerializer
from company.models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'phone_number', 'email']
        read_only_fields = ['id']
