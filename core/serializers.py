from rest_framework import serializers
from core.models import Project, Task, User, Company

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
    
class UserProfileSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'company']
    
    def get_company(self, obj):
        if hasattr(obj, 'company'):
            return obj.company.name
        return None
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'project', 'assigned_to', 'status', 'priority', 'deadline', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
