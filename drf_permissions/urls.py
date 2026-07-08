from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemHealthView, CustomTokenObtainPairView, UserProfileView, CorporateSecureDashboardView,
    AgentEscalationQueueView, SystemConfigView, CustomerSupportPortalView, TransactionViewSet,
    SecureDocumentViewSet
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'documents', SecureDocumentViewSet, basename='docs')

urlpatterns = [
    path("health/", SystemHealthView.as_view(), name = 'system-health'),
    path("login/", CustomTokenObtainPairView.as_view(), name = 'login'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name= 'profile'),
    path('security/', CorporateSecureDashboardView.as_view()),
    path('agent/', AgentEscalationQueueView.as_view()),
    path('sys-config/', SystemConfigView.as_view()),
    path('portal/', CustomerSupportPortalView.as_view()),
    path('',include(router.urls)),
]