from rest_framework import serializers
from .models import User, Account, Transaction

class UserNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "full_name",
            "email"
        ]


class AccountNestedSerializer(serializers.ModelSerializer):

    user = UserNestedSerializer()

    class Meta:
        model = Account
        fields = [
            "account_number",
            "user"
        ]

class TransactionCreateSerializer(serializers.ModelSerializer):

    account = AccountNestedSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        user_data = account_data.pop("user")
        
        user = User.objects.create(**user_data)
        account = Account.objects.create(user = user, **account_data)
        transaction = Transaction.objects.create(account= account, **validated_data)

        return transaction
    
    def update(self, instance, validated_data):
        account_data = validated_data.pop("account", None)

        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()

        if account_data:
            account_instance = instance.account
            for attr, value in account_data.items():
                setattr(account_instance, attr, value)
            account_instance.save()
        
        return instance