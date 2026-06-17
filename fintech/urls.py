from django.urls import path

from .views import (
    AccountAPIView,
    TransactionAPIView,
    MerchantAPIView,
    CardAPIView
)

urlpatterns = [

    path("accounts/",AccountAPIView.as_view()),
    path("accounts/<int:pk>/",AccountAPIView.as_view()),
    path("transactions/",TransactionAPIView.as_view()),
    path("transactions/<int:pk>/",TransactionAPIView.as_view()),
    path("merchants/",MerchantAPIView.as_view()),
    path("merchants/<int:pk>/",MerchantAPIView.as_view()),
    path("cards/",CardAPIView.as_view())
]