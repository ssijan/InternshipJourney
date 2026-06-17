from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

from .managers import ActiveMerchantManager


class Account(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts"
    )

    account_number = models.CharField(
        max_length=20,
        unique=True
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["account_number"]),
        ]

    def __str__(self):
        return self.account_number


class Merchant(models.Model):
    name = models.CharField(max_length=255)

    category = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_merchants = ActiveMerchantManager()

    class Meta:
        indexes = [
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.name


class Card(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="cards"
    )

    card_number = models.CharField(
        max_length=16,
        unique=True
    )

    expiry_date = models.DateField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.card_number


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        CREDIT = "CREDIT", "Credit"
        DEBIT = "DEBIT", "Debit"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["transaction_type"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="positive_transaction_amount"
            )
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"