from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserCompanySignupSerializer
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