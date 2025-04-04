from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from core.models import Project, Task, Invite
from core.permissions import IsCompanyAdmin
from core.serializers import AcceptInviteSerializer, InviteSerializer, ProjectSerializer, TaskSerializer, UserCompanySignupSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserCompanySignupView(APIView):
    """
    View to handle user and company signup.
    """
    def post(self, request):
        serializer = UserCompanySignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                "message": "Signup successful",
                "user_email": data['user'].email,
                "company": data['company'].name,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProtectedHelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "message": "Hello {user.name}, you're authenticated!",
            "email": user.email,
        })
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company, created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class InviteViewSet(viewsets.ModelViewSet):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get_queryset(self):
        return Invite.objects.filter(company=self.request.user.company)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite = serializer.save()
        return Response({
            "message": "Invite sent successfully",
            "invite_link": invite.get_invite_link(),
        }, status=status.HTTP_201_CREATED)
    
class AcceptInviteView(APIView):
    def post(self, request, token=None):
        serializer = AcceptInviteSerializer(data=request.data, context={'token': token})
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)