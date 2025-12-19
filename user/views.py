from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from library_app.utils import wrap_response
from rest_framework.permissions import IsAuthenticated , AllowAny
from user.models import User

class RegisterAPIView(APIView):
    """API endpoint for user registration"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Register a new user
        
        Request body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "password2": "string",
            "first_name": "string",
            "last_name": "string",
        }
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return wrap_response(
                success=True, 
                code="user_created", 
                message='User registered successfully', 
                data={
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status_code=status.HTTP_201_CREATED
            )
        
        return wrap_response(success=False, code="user_creation_failed", message='User registration failed', errors=serializer.errors)


class LoginAPIView(APIView):
    """API endpoint for user login"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Login user and return JWT tokens
        
        Request body:
        {
            "username": "string",
            "password": "string"
        }
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return wrap_response(
                success=True,
                code="user_logged_in",
                message='Login successful',
                data={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            )
        
        return wrap_response(
            success=False,
            code="user_login_failed",
            message='Login failed',
            errors=serializer.errors
        )

class ProfileAPIView(APIView):
    """API endpoint for user profile"""
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        """Get user profile"""
        user = request.user
        return wrap_response(
            success=True,
            code="user_profile_retrieved",
            message='User profile retrieved successfully',
            data=UserSerializer(user).data
        )

class UsersAPIView(APIView):
    """API endpoint for user profile"""
    permission_classes = [AllowAny]  
    
    def get(self, request):
        """Get user profile"""
        users = User.objects.filter(is_superuser=False)
        return wrap_response(
            success=True,
            code="users_retrieved",
            message='Users retrieved successfully',
            data=UserSerializer(users, many=True).data
        )