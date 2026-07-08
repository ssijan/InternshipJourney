from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from guardian.shortcuts import assign_perm
from django.shortcuts import get_object_or_404

from .permissions import (
    IsAccountOwner, IsStaffUser, IsActiveAccount, IsVerifiedUser,
    HasRoleAdmin, HasRoleAgent, IsTransactionOwnerOrStaff, GuardianObjectPermissions
)
from .models import Profile, Transaction, SecureDocument
from .serializers import CustomTokenObtainPairSerializer, TransactionSerializer, SecureDocumentSerializer

#Login views
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#Accessible  for all authenticated user
class SystemHealthView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        data = {"message":"Getting all data..."}
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not IsStaffUser():
            raise PermissionDenied("Only staff accounts can update system health.")
        return Response({"message": "User Created sucessfully!"}, status= status.HTTP_201_CREATED)
    

# Only Profile Owner can see his/her profile else deny
class UserProfileView(APIView):
    permission_classes = [IsAccountOwner]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)

        self.check_object_permissions(request, profile)
        # print(request.user.is_authenticated)

        return Response({
            "profile_id": profile.id,
            "owner": profile.user.username,
            "bio": profile.bio,
            "location": profile.location
        }, status=status.HTTP_200_OK)
    

# Only active and verified user or staff can access
class CorporateSecureDashboardView(APIView):
    permission_classes = [IsStaffUser | (IsActiveAccount & IsVerifiedUser)]

    def get(self, request):
        return Response(
            {"secure_data": "Sensors nominal. Corporate operations clear."}, 
            status=status.HTTP_200_OK
        )


'''
AgentEscalationQueueView -> Only for Agent
SystemConfigView -> Only for Admin
CustomerSupportPortalView -> Both for Admin and Agent
Customer's are blocked from all 
'''

class AgentEscalationQueueView(APIView):
    permission_classes = [HasRoleAgent]
    def get(self, request):
        return Response({"tickets": ["Ticket #104", "Ticket #208"]}, status=status.HTTP_200_OK)
    
class SystemConfigView(APIView):
    permission_classes = [HasRoleAdmin]
    def get(self, request):
        return Response({"status": "Cluster settings updated"}, status=status.HTTP_200_OK)
    
class CustomerSupportPortalView(APIView):
    permission_classes = [HasRoleAdmin | HasRoleAgent]

    def get(self, request):
        return Response({
            "message": "Welcome to the Internal Customer Support Portal.",
            "authorized_user": request.user.username,
            "role": request.user.role
        }, status=status.HTTP_200_OK)
    


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsTransactionOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'role', None) in ['ADMIN', 'AGENT']:
            return Transaction.objects.select_related('user').all()
        
        return Transaction.objects.select_related('user').filter(user = user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    @action(detail=True, methods=['post'], url_path='dispute')
    def dispute(self, request, pk = None):
        transection = self.get_object()

        if transection.status == Transaction.Status.DISPUTED:
            return Response(
                {"error": "This transaction is already disputed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transection.status = Transaction.Status.DISPUTED
        transection.save()

        return Response({
            "message": f"Dispute file successfully opened for transaction #{transaction.id}.",
            "current_status": transaction.status
        }, status=status.HTTP_200_OK)




# django-guardian

class SecureDocumentViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & GuardianObjectPermissions]
    queryset = SecureDocument.objects.all()
    serializer_class = SecureDocumentSerializer

    def perform_create(self, serializer):
        instance = serializer.save(user = self.request.user)
        assign_perm('view_securedocument', self.request.user, instance)
        assign_perm('edit_securedocument', self.request.user, instance)