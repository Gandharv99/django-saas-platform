from rest_framework_simplejwt.views import TokenObtainPairView
from core.auth.serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer