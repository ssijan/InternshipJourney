import os
import django
from datetime import date

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)


django.setup()


from django.contrib.auth.models import User
from fintech.models import (
    Account,
    Card,
    Merchant,
    Transaction,
)



def seed_data():

    print("Creating sample data...")

    user1, _ = User.objects.get_or_create(
        username="john",
        defaults={
            "email": "john@gmail.com"
        }
    )

    user2, _ = User.objects.get_or_create(
        username="alice",
        defaults={
            "email": "alice@gmail.com"
        }
    )

    acc1, _ = Account.objects.get_or_create(
        user=user1,
        account_number="ACC1001",
        defaults={
            "balance": 50000
        }
    )

    acc2, _ = Account.objects.get_or_create(
        user=user2,
        account_number="ACC1002",
        defaults={
            "balance": 120000
        }
    )

    amazon, _ = Merchant.objects.get_or_create(
        name="Amazon",
        defaults={
            "category": "E-Commerce"
        }
    )

    starbucks, _ = Merchant.objects.get_or_create(
        name="Starbucks",
        defaults={
            "category": "Food"
        }
    )

    Card.objects.get_or_create(
        account=acc1,
        card_number="1111222233334444",
        defaults={
            "expiry_date": date(2028, 12, 31)
        }
    )

    Card.objects.get_or_create(
        account=acc2,
        card_number="5555666677778888",
        defaults={
            "expiry_date": date(2029, 12, 31)
        }
    )

    Transaction.objects.get_or_create(
        account=acc1,
        merchant=amazon,
        amount=2500,
        transaction_type="DEBIT"
    )

    Transaction.objects.get_or_create(
        account=acc1,
        merchant=starbucks,
        amount=500,
        transaction_type="DEBIT"
    )

    Transaction.objects.get_or_create(
        account=acc2,
        merchant=amazon,
        amount=10000,
        transaction_type="DEBIT"
    )

    Transaction.objects.get_or_create(
        account=acc2,
        amount=15000,
        transaction_type="CREDIT"
    )

    print("Sample data created successfully.")

if __name__ == "__main__":
    seed_data()