from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from core.filters import TaskFilter
from core.models import Project, Task, Invite, User
from core.permissions import IsAdminOrSeniorMember, IsCompanyAdmin, TaskAccessPermission
from core.serializers import AcceptInviteSerializer, InviteSerializer, ProjectSerializer, TaskSerializer, UserCompanySignupSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

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
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company, created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskAccessPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    def get_queryset(self):
        return Task.objects.filter(project__company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSeniorMember()]
        return [IsAuthenticated()]


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
    
class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeniorMember]

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company).exclude(id=self.request.user.id)


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(project__company=user.company)
        # apply filters if any are provided
        project_id = request.query_params.get('project')
        assigned_to = request.query_params.get('assigned_to')
        deadline_min = request.query_params.get('deadline_min')
        deadline_max = request.query_params.get('deadline_max')
        if project_id:
            tasks = tasks.filter(project_id=project_id)
        if assigned_to:
            tasks = tasks.filter(assigned_to=assigned_to)
        if deadline_min:
            tasks = tasks.filter(deadline__gte=deadline_min)
        if deadline_max:
            tasks = tasks.filter(deadline__lte=deadline_max)
        # stats
        total_projects = Project.objects.filter(company=user.company).count()
        total_tasks = tasks.count()
        completed = tasks.filter(status='done').count()
        in_progress = tasks.filter(status='in_progress').count()
        todo = tasks.filter(status='todo').count()
        completed_percentage = round((completed / total_tasks * 100), 2) if total_tasks > 0 else 0.0
        
        return Response({
            "stats": {
                "total_tasks": total_tasks,
                "completed": completed,
                "in_progress": in_progress,
                "todo": todo,
                "completed_percentage": completed_percentage,
            },
            "meta":{
                "total_projects": total_projects,
            }
        })