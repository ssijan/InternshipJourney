# models.py

from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name
    

class Account(models.Model):

    class AccountType(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    user = models.ForeignKey(
        User,
        related_name="accounts",
        on_delete=models.CASCADE
    )

    account_number = models.CharField(
        max_length=20,
        unique=True
    )

    balance_usd = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices
    )

    card_number = models.CharField(
        max_length=16
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.account_number


class Transaction(models.Model):

    class Type(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAW = "withdraw", "Withdraw"

    account = models.ForeignKey(
        Account,
        related_name="transactions",
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=Type.choices
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )