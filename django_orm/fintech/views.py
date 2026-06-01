from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Account,
    Transaction,
    Merchant,
    Card
)

from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    MerchantSerializer,
    CardSerializer
)


# ACCOUNT API

class AccountAPIView(APIView):

    def get(self, request, pk=None):

        if pk:
            account = get_object_or_404(
                Account.objects
                .select_related("user")
                .prefetch_related(
                    "cards",
                    "transactions"
                ),
                pk=pk
            )

            serializer = AccountSerializer(account)

            return Response(serializer.data)

        accounts = (
            Account.objects
            .select_related("user")
            .prefetch_related(
                "cards",
                "transactions"
            )
        )

        serializer = AccountSerializer(
            accounts,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = AccountSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


    def put(self, request, pk):

        account = get_object_or_404(
            Account,
            pk=pk
        )

        serializer = AccountSerializer(
            account,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def patch(self, request, pk):

        account = get_object_or_404(
            Account,
            pk=pk
        )

        serializer = AccountSerializer(
            account,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def delete(self, request, pk):

        account = get_object_or_404(
            Account,
            pk=pk
        )

        account.delete()

        return Response(
            {
                "message": "Account deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )


# TRANSACTION API

class TransactionAPIView(APIView):

    def get(self, request, pk=None):

        if pk:

            transaction = get_object_or_404(
                Transaction.objects.select_related(
                    "account",
                    "merchant"
                ),
                pk=pk
            )

            serializer = TransactionSerializer(
                transaction
            )

            return Response(serializer.data)

        transactions = (
            Transaction.objects
            .select_related(
                "account",
                "merchant"
            )
        )

        serializer = TransactionSerializer(
            transactions,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = TransactionSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


    def put(self, request, pk):

        transaction = get_object_or_404(
            Transaction,
            pk=pk
        )

        serializer = TransactionSerializer(
            transaction,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def patch(self, request, pk):

        transaction = get_object_or_404(
            Transaction,
            pk=pk
        )

        serializer = TransactionSerializer(
            transaction,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def delete(self, request, pk):

        transaction = get_object_or_404(
            Transaction,
            pk=pk
        )

        transaction.delete()

        return Response(
            {
                "message": "Transaction deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )


# MERCHANT API

class MerchantAPIView(APIView):

    def get(self, request, pk=None):

        if pk:

            merchant = get_object_or_404(
                Merchant,
                pk=pk
            )

            serializer = MerchantSerializer(
                merchant
            )

            return Response(serializer.data)

        merchants = Merchant.objects.all()

        serializer = MerchantSerializer(
            merchants,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = MerchantSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


    def put(self, request, pk):

        merchant = get_object_or_404(
            Merchant,
            pk=pk
        )

        serializer = MerchantSerializer(
            merchant,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def patch(self, request, pk):

        merchant = get_object_or_404(
            Merchant,
            pk=pk
        )

        serializer = MerchantSerializer(
            merchant,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def delete(self, request, pk):

        merchant = get_object_or_404(
            Merchant,
            pk=pk
        )

        merchant.delete()

        return Response(
            {
                "message": "Merchant deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

class CardAPIView(APIView):
    def get(self, request):
        card = Card.objects.all()

        serializer = CardSerializer(card, many = True)

        return Response(serializer.data)