
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import AccountDetailSerializer, AccountListSerializer
from .models import BankAccount

from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
 
'''
        API-VIEW
'''
class AccountListCreateAPIView(APIView):
    """
    GET  /api/v1/accounts/    list accounts for logged-in user
    POST /api/v1/accounts/    create a new account
    """
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        accounts = BankAccount.objects.filter(owner=request.user)
        serializer = AccountListSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def post(self, request):
        serializer = AccountDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class AccountRetrieveUpdateDestroyAPIView(APIView):
    """
    GET    /api/v1/accounts/<pk>/   retrieve
    PUT    /api/v1/accounts/<pk>/   full update
    PATCH  /api/v1/accounts/<pk>/   partial update
    DELETE /api/v1/accounts/<pk>/   delete
    """
    permission_classes = [IsAuthenticated]
 
    def get_object(self, pk, user):
        return get_object_or_404(BankAccount, pk=pk, owner=user)
 
    def get(self, request, pk):
        account = self.get_object(pk, request.user)
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data)
 
    def put(self, request, pk):
        account = self.get_object(pk, request.user)
        serializer = AccountDetailSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def patch(self, request, pk):
        account = self.get_object(pk, request.user)
        serializer = AccountDetailSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        account = self.get_object(pk, request.user)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 


'''
        GenericAPIView + Mixins
'''

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
 
 
class AccountListCreateGenericView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    GET  /api/v2/accounts/   → list
    POST /api/v2/accounts/   → create
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDetailSerializer
 
    def get_queryset(self):
        return BankAccount.objects.filter(owner=self.request.user)
 
    def get_serializer_class(self):
        if self.request.method == "GET":
            return AccountListSerializer
        return AccountDetailSerializer
 
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
 
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) 
 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 
 
class AccountRetrieveUpdateDestroyGenericView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    GET    /api/v2/accounts/<pk>/
    PUT    /api/v2/accounts/<pk>/
    PATCH  /api/v2/accounts/<pk>/
    DELETE /api/v2/accounts/<pk>/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDetailSerializer
 
    def get_queryset(self):
        return BankAccount.objects.filter(owner=self.request.user)
 
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
 
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
 
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
 
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


'''
    ModelViewSet
'''

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
 
 
class AccountViewSet(ModelViewSet):
    """
    Automatically provides:
      list      → GET  /api/v3/accounts/
      create    → POST /api/v3/accounts/
      retrieve  → GET  /api/v3/accounts/<pk>/
      update    → PUT  /api/v3/accounts/<pk>/
      partial_update → PATCH /api/v3/accounts/<pk>/
      destroy   → DELETE /api/v3/accounts/<pk>/
    """
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        return BankAccount.objects.filter(owner=self.request.user)
 
    def get_serializer_class(self):
        if self.action == "list":
            return AccountListSerializer
        return AccountDetailSerializer
 
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
 

    @action(detail=True, methods=["post"], url_path="freeze")
    def freeze(self, request, pk=None):
        account = self.get_object()
        account.status = "frozen"
        account.save()
        return Response({"status": "Account frozen"}, status=status.HTTP_200_OK)