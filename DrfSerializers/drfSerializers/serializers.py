from rest_framework import serializers
from .models import User, Account, Transaction
from .fields import MaskedCardField, MoneyField

#1
class UserBasicSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    def validate_email(self, value):

        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError("Only gmail accounts allowed.")

        return value

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.full_name = validated_data.get("full_name",instance.full_name)
        instance.email = validated_data.get("email",instance.email)
        instance.save()

        return instance
    
#2
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

#3
class AccountSerializer(serializers.ModelSerializer):

    balance = MoneyField(source="balance_usd")
    card_number = MaskedCardField()

    class Meta:
        model = Account

        fields = ["id","account_number","account_type","balance","card_number"]

    def validate_account_number(self, value):

        if len(value) < 10:
            raise serializers.ValidationError("Account number too short.")

        return value
    
#4
class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction

        fields = "__all__"

    def validate(self, attrs):

        account = attrs["account"]
        amount = attrs["amount"]
        tx_type = attrs["transaction_type"]

        if (tx_type == "withdraw" and amount > account.balance_usd):

            raise serializers.ValidationError("Insufficient balance")

        return attrs
    

#5
class AccountDetailSerializer(serializers.ModelSerializer):

    balance = MoneyField(source="balance_usd")
    transaction_count = serializers.SerializerMethodField()
    last_active = serializers.SerializerMethodField()

    class Meta:
        model = Account

        fields = [
            "id",
            "account_number",
            "balance",
            "transaction_count",
            "last_active",
        ]
    
    
    def get_transaction_count(self, obj):
        return obj.transactions.count()

    def get_last_active(self, obj):
        
        last_tx = obj.transactions.order_by("-created_at").first()

        return last_tx.created_at if last_tx else None