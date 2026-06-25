from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import (
    RegisterAPIView, 
    CustomTokenObtainPairView, 
    NativeTokenGenerationView,
    SessionTrackerListView,
    RevokeSessionDestroyView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth_login_jwt'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='auth_logout'),
    path('debug-drf-token/', NativeTokenGenerationView.as_view(), name='auth_drf_token'),
    path('sessions/', SessionTrackerListView.as_view(), name='session_list'),
    path('sessions/<int:pk>/revoke/', RevokeSessionDestroyView.as_view(), name='session_revoke'),
]