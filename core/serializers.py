from rest_framework import serializers
from core.models import User, Company

class UserCompanySignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=255)
    company_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        name = validated_data['name']
        company_name = validated_data['company_name']

        user = User.objects.create_user(email=email, password=password, name=name)
        company = Company.objects.create(owner=user, name=company_name)

        return {
            'user': user,
            'company': company
        }