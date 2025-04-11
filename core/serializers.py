from django.utils import timezone
from rest_framework import serializers
from core.models import Invite, Project, Task, User, Company

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

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['id', 'email', 'role', 'token', 'accepted', 'expires_at', 'created_at']
        read_only_fields = ['id', 'token', 'accepted', 'expires_at', 'created_at']

    def validate_email(self, value):
        user = self.context['request'].user
        if Invite.objects.filter(email=value, company=user.company, accepted=False).exists():
            raise serializers.ValidationError("User already invited.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        invite = Invite.objects.create(email=validated_data['email'], role=validated_data['role'], invited_by=user, company=user.company) 
        return invite
    
class AcceptInviteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        token = self.context.get('token')
        try:
            invite = Invite.objects.get(token=token, accepted=False)
        except Invite.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired invite token.")
        if invite.expires_at < timezone.now():
            raise serializers.ValidationError("Invite token has expired.")
        self.context['invite'] = invite
        return attrs
    
    def create(self, validated_data):
        invite = self.context['invite']
        user = User.objects.create_user(
            email=invite.email, 
            password=validated_data['password'], 
            name=validated_data['name'],
            role=invite.role,
            company = invite.company
        )
        invite.accepted = True
        invite.save()
        return user
    

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role']