from django.shortcuts import render
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LogoutSerializer, RefreshTokenSerializer, UserSerializer, UpdateUserSerializer,\
    ChangePasswordSerializer, LoginSerializer

class CreateUserAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.all()
    
    
class UpdateUserInfoAPIView(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['put', 'patch']
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'success': True,
            'message': 'User information updated successfully!',
            'data': response.data  
        }, status=200)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            'success': True,
            'message': 'User information updated successfully!',
            'data': response.data 
        }, status=200)

class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the input data
        serializer.save()  # Save the updated user instance
        
        return Response({
            "success": "Your password has been updated successfully!"
        }, status=status.HTTP_200_OK)
        

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        # Call the parent method to generate tokens
        response = super().post(request, *args, **kwargs)
        
        # Check if both 'access' and 'refresh' tokens are in the response
        if 'access' in response.data:
            print("Access Token:", response.data['access'])
        else:
            print("No Access Token found.")
        
        if 'refresh' in response.data:
            print("Refresh Token:", response.data['refresh'])
        else:
            print("No Refresh Token found.")
        
        # Return the response as usual
        return response

class LoginRefreshAPIView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer
    
class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'success':True,
                'message':'You successfully logged out!'
            }, status=205)
        except TokenError:
            return Response(status=400)
        

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        user = request.user
        user_info = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role, 
        }
        
        
        return Response({
            'user_info': user_info,
            'message': 'Dashboard data fetched successfully.'
        })