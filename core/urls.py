from django.urls import path
from core.views import TaskViewSet, UserCompanySignupView, UserProfileView
from core.views import ProjectViewSet
from core.views import ProtectedHelloView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('signup/', UserCompanySignupView.as_view(), name='signup'),
    path('protected/', ProtectedHelloView.as_view(), name='protected'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
urlpatterns += router.urls