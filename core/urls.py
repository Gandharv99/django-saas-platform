from django.urls import path
from core.views import AcceptInviteView, UserCompanySignupView, UserProfileView
from core.views import ProjectViewSet, TaskViewSet, InviteViewSet
from core.views import ProtectedHelloView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'invites', InviteViewSet, basename='invite')

urlpatterns = [
    path('signup/', UserCompanySignupView.as_view(), name='signup'),
    path('protected/', ProtectedHelloView.as_view(), name='protected'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('invite/accept/<uuid:token>/', AcceptInviteView.as_view(), name='accept-invite'),
]
urlpatterns += router.urls