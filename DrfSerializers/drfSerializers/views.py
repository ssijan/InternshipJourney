from django.shortcuts import render
from .models import Account, User, Transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import UserSerializer, AccountSerializer, TransactionSerializer
from .nested_serializers import TransactionCreateSerializer
from .bulk_serializers import TransactionBulkSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
            return TransactionCreateSerializer
        return TransactionSerializer


class TransactionBulkViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionBulkSerializer

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        serializer = TransactionBulkSerializer(data = request.data , many = True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=["patch"])
    def bulk_update(self, request):
        # print(request.data[0])
        ids = [item["id"] for item in request.data]
        # print(ids)
        queryset = Transaction.objects.filter(id__in = ids)

        seralizer = TransactionBulkSerializer(
            queryset,
            data = request.data,
            many = True,
            partial= True
        )
        seralizer.is_valid(raise_exception=True)
        
        seralizer.save()
        return Response(
            seralizer.data,
            status=status.HTTP_200_OK
        )