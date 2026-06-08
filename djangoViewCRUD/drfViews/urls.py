from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    AccountListCreateAPIView, 
    AccountRetrieveUpdateDestroyAPIView,
    AccountListCreateGenericView,
    AccountRetrieveUpdateDestroyGenericView,
    AccountViewSet,
    RegisterAPIView,

)

urlpatterns = [
    path("auth/login/",TokenObtainPairView.as_view(),name="login"),
    path("auth/token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("auth/register/",RegisterAPIView.as_view(),name="register",),

    # for APIView
    path("v1/accounts/", AccountListCreateAPIView.as_view()),
    path("v1/accounts/<int:pk>/", AccountRetrieveUpdateDestroyAPIView.as_view()),

    #for genericView
    path("v2/accounts/", AccountListCreateGenericView.as_view()),
    path("v2/accounts/<int:pk>/", AccountRetrieveUpdateDestroyGenericView.as_view()),
]

# for ModelViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("v3/accounts", AccountViewSet, basename="account")
urlpatterns += router.urls