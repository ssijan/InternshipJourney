
from rest_framework import status
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from .models import UserSessionTracker
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "detail": "User created successfully.",
                "user": {
                    "email": user.email,
                    "account_id": user.account_id,
                    "role": user.role
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    
class CustomTokenObtainPairView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data = request.data, context={'request':request})

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class NativeTokenGenerationView(APIView):
    parser_classes = [IsAuthenticated]
    def post(self, request):
            token, _ = Token.objects.get_or_create(user=request.user)
            return Response({"drf_static_token": token.key}, status=status.HTTP_200_OK)
    

class SessionTrackerListView(APIView):
     permission_classes = [IsAuthenticated]

     def get(self, request):
        act_sessions = UserSessionTracker.objects.filter(
            user = request.user,
            expires_at__gt = now()
        ) 

        session_payload = [
            {
                "session_id": s.id,
                "device": s.device_name,
                "ip_address": s.ip_address,
                "login_time": s.created_at,
                "expires_at": s.expires_at
            } for s in act_sessions
        ]

        return Response(session_payload, status=status.HTTP_200_OK)
     


class RevokeSessionDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            session_tracker = UserSessionTracker.objects.get(id=pk, user=request.user)
            target_token = OutstandingToken.objects.filter(jti=session_tracker.refresh_jti).first()

            if target_token:
                BlacklistedToken.objects.get_or_create(token=target_token)
            
            session_tracker.delete()
            return Response(
                {"detail": f"Session tracking record {pk} and related JWT have been blacklisted."}, 
                status=status.HTTP_200_OK
            )
            
        except UserSessionTracker.DoesNotExist:
            return Response(
                {"error": "The targeted active session track record was not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        