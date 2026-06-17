from rest_framework import serializers
from .models import BankAccount
from django.contrib.auth.models import User

 
class AccountListSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(source="owner.username", read_only=True)
 
    class Meta:
        model = BankAccount
        fields = ["id", "account_number", "account_type", "balance", "status", "owner_username"]
 
 
class AccountDetailSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(source="owner.username", read_only=True)
 
    class Meta:
        model = BankAccount
        fields = "__all__"
        read_only_fields = ["id", "owner", "created_at", "updated_at"]




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )