from django.urls import path
from core.views import UserCompanySignupView
from core.views import ProtectedHelloView

urlpatterns = [
    path('signup/', UserCompanySignupView.as_view(), name='signup'),
    path('protected/', ProtectedHelloView.as_view(), name='protected'),
]
