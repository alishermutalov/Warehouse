from typing import Any, Dict
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,  TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from .models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, required=False)
    role = serializers.CharField(read_only=True, required=False)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id','role', 'username','password','confirm_password']
    
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise ValidationError({
                "message":"Password and Confirm Password do not match!"
            })
        if password:
            validate_password(password)
        return attrs
    
    def validate_username(self, username):
        if User.objects.filter(username__iexact=username):
            raise ValidationError({
                "message":"This username alredy taken!"
            })
        if len(username)<4 or len(username)>32:
            raise ValidationError({
                'message':'Username must be more than 4 characters and less than 32 characters'
            })
        if username.isdigit():
            raise ValidationError({
                'message':'This username is entirely numeric'
            })
        return username
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['first_name','last_name']
        
    def validate(self, attrs):
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        
        if first_name:
            if not first_name.isalpha():
                raise ValidationError("First Name should consist of only letters")
        if last_name:
            if not last_name.isalpha():
                raise ValidationError("Last Name should consist of only letters")
        return attrs
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()  
        
        return instance 
    
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)
    
    def validate_current_password(self, value):
        user = self.context['request'].user 
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate(self, attrs):
        password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_new_password')
        
        if password != confirm_password:
            raise ValidationError({
                "message":"New Password and Confirm New Password do not match!"
            })
        
        validate_password(password)
        return attrs
    
    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password) 
        user.save() 
        

class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        
        user = authenticate(username=username, password=password)
        attrs = self.user.token()
        attrs['full_name']=self.user.full_name
        return attrs
    

class RefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        acces_token_instance = AccessToken(data["access"])
        user_id = acces_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()