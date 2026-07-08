from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsActiveAccount, IsVerifiedUser, HasRoleAdmin, HasRoleAgent
from .models import Transaction
from .serializers import TransactionSerializer
from .permissions import IsTransactionOwnerOrStaff

class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated & IsActiveAccount & IsVerifiedUser & (HasRoleAdmin | HasRoleAgent | IsTransactionOwnerOrStaff)]

    def get_queryset(self):
        user = self.request.user
        role = self.request.auth.get('role') if self.request.auth else getattr(user, 'role', None)

        if role in ['ADMIN', 'AGENT']:
            return Transaction.objects.all().select_related('user')
        return Transaction.objects.filter(user=user).select_related('user')

    @action(detail=True, methods=['post'], url_path='dispute')
    def dispute(self, request, pk=None):
        transaction = self.get_object()
        transaction.is_disputed = True
        transaction.save()
        return Response(
            {"message": f"Transaction {transaction.reference} successfully placed in dispute status."},
            status=status.HTTP_200_OK
        )