from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import Transaction, SecureDocument

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role
        token['is_verified'] = user.is_verified
        token['username'] = user.username

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['role'] = self.user.role
        data['is_verified'] = self.user.is_verified
        data['username'] = self.user.username
        return data



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'merchant', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']



class SecureDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureDocument
        fields = ['id', 'title', 'confidential_content']
        read_only_fields = ['user']