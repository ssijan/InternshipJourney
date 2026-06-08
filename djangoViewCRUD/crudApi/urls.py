from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import (
    AccountViewSet,
    TransactionViewSet
)

router = DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"transactions", TransactionViewSet, basename="transaction")
 
urlpatterns = [
    path("api/auth/token/",TokenObtainPairView.as_view(),name="token"),
    path("api/auth/token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("api/", include(router.urls)),
]