from rest_framework.routers import DefaultRouter
from .views import(
    UserViewSet,
    AccountViewSet,
    TransactionBulkViewSet,
    TransactionViewSet
)
router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'TransactionsBulk', TransactionBulkViewSet, basename='transaction-bulk')

urlpatterns = router.urls