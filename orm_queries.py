from django.utils import timezone
from datetime import timedelta

from django.db.models import (
    Count,
    Sum,
    Avg,
    Max,
    Min,
    F,
    Q,
    Case,
    When,
    Value,
    CharField,
    OuterRef,
    Subquery,
)

from fintech.models import (
    User,
    Account,
    Transaction,
    Card,
    Merchant,
)



class ORMQueries:

    @staticmethod
    def separator(title):
        print("\n" + "=" * 70)
        print(title)
        print("=" * 70)


    # 1. Get all accounts

    @staticmethod
    def query_1():

        ORMQueries.separator("QUERY 1 - ALL ACCOUNTS")

        accounts = Account.objects.all()

        for account in accounts:
            print(
                f"Account: {account.account_number}"
                f" | Balance: {account.balance}"
            )


    # 2. Accounts with balance > 10000

    @staticmethod
    def query_2():

        ORMQueries.separator("QUERY 2 - BALANCE GREATER THAN 10000")

        accounts = Account.objects.filter(
            balance__gt=10000
        )

        for account in accounts:
            print(account.account_number)


    # 3. Transactions greater than 5000

    @staticmethod
    def query_3():

        ORMQueries.separator("QUERY 3 - LARGE TRANSACTIONS")

        transactions = Transaction.objects.filter(
            amount__gt=5000
        )

        for transaction in transactions:
            print(
                transaction.id,
                transaction.amount
            )


    # 4. Q Objects

    @staticmethod
    def query_4():

        ORMQueries.separator("QUERY 4 - Q OBJECTS")

        transactions = Transaction.objects.filter(
            Q(amount__gt=5000)
            |
            Q(transaction_type="CREDIT")
        )

        for transaction in transactions:
            print(
                transaction.id,
                transaction.transaction_type,
                transaction.amount
            )


    # 5. F Expression

    @staticmethod
    def query_5():

        ORMQueries.separator("QUERY 5 - F EXPRESSION")

        Account.objects.update(
            balance=F("balance") + 100
        )

        print(
            "Added 100 to all account balances."
        )


    # 6. Count Transactions Per Account

    @staticmethod
    def query_6():

        ORMQueries.separator(
            "QUERY 6 - COUNT TRANSACTIONS"
        )

        accounts = Account.objects.annotate(
            total_transactions=Count(
                "transactions"
            )
        )

        for account in accounts:

            print(
                account.account_number,
                account.total_transactions
            )


    # 7. Sum of Transactions

    @staticmethod
    def query_7():

        ORMQueries.separator(
            "QUERY 7 - TOTAL AMOUNT"
        )

        result = Transaction.objects.aggregate(
            total_amount=Sum("amount")
        )

        print(result)


    # 8. Average Transaction

    @staticmethod
    def query_8():

        ORMQueries.separator(
            "QUERY 8 - AVERAGE AMOUNT"
        )

        result = Transaction.objects.aggregate(
            average_amount=Avg("amount")
        )

        print(result)


    # 9. Highest Transaction

    @staticmethod
    def query_9():

        ORMQueries.separator(
            "QUERY 9 - MAX TRANSACTION"
        )

        result = Transaction.objects.aggregate(
            max_amount=Max("amount")
        )

        print(result)


    # 10. Lowest Transaction

    @staticmethod
    def query_10():

        ORMQueries.separator(
            "QUERY 10 - MIN TRANSACTION"
        )

        result = Transaction.objects.aggregate(
            min_amount=Min("amount")
        )

        print(result)


    # 11. Merchant Transaction Count

    @staticmethod
    def query_11():

        ORMQueries.separator(
            "QUERY 11 - MERCHANT TRANSACTION COUNT"
        )

        merchants = Merchant.objects.annotate(
            total_transactions=Count(
                "transactions"
            )
        )

        for merchant in merchants:

            print(
                merchant.name,
                merchant.total_transactions
            )


    # 12. Conditional Expression

    @staticmethod
    def query_12():

        ORMQueries.separator(
            "QUERY 12 - CASE WHEN"
        )

        transactions = (
            Transaction.objects
            .annotate(
                category=Case(
                    When(
                        amount__gt=10000,
                        then=Value("Large")
                    ),
                    default=Value("Normal"),
                    output_field=CharField(),
                )
            )
        )

        for transaction in transactions:

            print(
                transaction.amount,
                transaction.category
            )


    # 13. select_related

    @staticmethod
    def query_13():

        ORMQueries.separator(
            "QUERY 13 - SELECT RELATED"
        )

        transactions = (
            Transaction.objects
            .select_related(
                "account",
                "merchant"
            )
        )

        for transaction in transactions:

            print(
                transaction.account.account_number,
                transaction.merchant.name
                if transaction.merchant
                else "No Merchant"
            )


    # 14. prefetch_related

    @staticmethod
    def query_14():

        ORMQueries.separator(
            "QUERY 14 - PREFETCH RELATED"
        )

        accounts = (
            Account.objects
            .prefetch_related(
                "transactions",
                "cards"
            )
        )

        for account in accounts:

            print(
                account.account_number
            )

            print(
                "Transactions:",
                account.transactions.count()
            )

            print(
                "Cards:",
                account.cards.count()
            )


    # 15. Subquery

    @staticmethod
    def query_15():

        ORMQueries.separator(
            "QUERY 15 - SUBQUERY"
        )

        latest_transaction = (
            Transaction.objects
            .filter(
                account=OuterRef("pk")
            )
            .order_by("-created_at")
        )

        accounts = (
            Account.objects
            .annotate(
                latest_amount=Subquery(
                    latest_transaction.values(
                        "amount"
                    )[:1]
                )
            )
        )

        for account in accounts:

            print(
                account.account_number,
                account.latest_amount
            )


    # 16. Cards Expiring Within 2 Years

    @staticmethod
    def query_16():

        ORMQueries.separator("QUERY 16 - CARDS EXPIRING WITHIN 2 YEARS")
        print("Total cards:", Card.objects.count())
        today = timezone.now().date()
        future_date = today + timedelta(days=365 * 2)

        cards = Card.objects.filter(
            expiry_date__lte=future_date
        ).select_related("account")

        if not cards.exists():
            print("No cards expiring within 2 years.")
            return

        for card in cards:
            print(
                f"Card: {card.card_number} | "
                f"Account: {card.account.account_number} | "
                f"Expiry: {card.expiry_date}"
            )

def run_all_queries():

    for i in range(1, 17):
        query = getattr(ORMQueries, f"query_{i}")
        query()