import uuid
from datetime import datetime, timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import UserSessionTracker


User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['email','password', 'role']

    def create(self, validated_data):
        validated_data['account_id'] = f"ACC-{uuid.uuid4().hex[:8].upper()}"
        return User.objects.create_user(**validated_data)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['account_id'] = user.account_id


        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh_token = RefreshToken(data['refresh'])
        jti = refresh_token['jti']

        request = self.context.get('request')
        device = 'Unknown Context'
        id = None

        if request:
            device = request.META.get('HTTP_USER_AGENT', 'Unknown Context')
            ip = request.META.get('REMOTE_ADDR')

        expiry_timestamp = refresh_token['exp']
        expiry_datetime = datetime.fromtimestamp(expiry_timestamp, tz=timezone.utc)

        UserSessionTracker.objects.create(
            user=self.user,
            refresh_jti=jti,
            device_name=device[:255],
            ip_address=ip,
            expires_at=expiry_datetime
        )
        
        return data