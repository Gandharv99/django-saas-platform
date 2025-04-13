from django.urls import path
from core.auth.views import CustomTokenObtainPairView
from core.views import AcceptInviteView, DashboardStatsView, UserCompanySignupView, UserProfileView
from core.views import ProjectViewSet, TaskViewSet, InviteViewSet, UserListViewSet
from core.views import ProtectedHelloView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'invites', InviteViewSet, basename='invite')
router.register(r'users', UserListViewSet, basename='user')

urlpatterns = [
    path('signup/', UserCompanySignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('protected/', ProtectedHelloView.as_view(), name='protected'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('invite/accept/<uuid:token>/', AcceptInviteView.as_view(), name='accept-invite'),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
urlpatterns += router.urls