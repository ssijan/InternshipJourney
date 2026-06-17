from rest_framework import serializers
from .models import Account, Transaction
 
class AccountListSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(source="owner.username", read_only=True)
 
    class Meta:
        model = Account
        fields = [
            "id", "account_number", "account_type",
            "balance", "status", "owner_username", "created_at",
        ]
        read_only_fields = ["id", "balance", "created_at"]
 
 
class AccountDetailSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(source="owner.username", read_only=True)
    transaction_count = serializers.SerializerMethodField()
 
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["id", "owner", "balance", "created_at", "updated_at"]
 
    def get_transaction_count(self, obj):
        return obj.transactions.count()
 
    def validate_account_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Account number must be numeric.")
        return value
 
 
class TransactionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            "id", "reference", "transaction_type", "amount",
            "status", "created_at",
        ]
 
 
class TransactionDetailSerializer(serializers.ModelSerializer):

    reversed_by_reference = serializers.SerializerMethodField()
 
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = [
            "id", "reference", "balance_before", "balance_after",
            "status", "reversed_by", "created_at",
        ]
 
    def get_reversed_by_reference(self, obj):
        if obj.reversed_by:
            return str(obj.reversed_by.reference)
        return None
 
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value
 
 
class StatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["reference", "transaction_type", "amount",
                  "balance_before", "balance_after", "description",
                  "status", "created_at"]
 