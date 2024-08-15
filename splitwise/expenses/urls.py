from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BalanceViewSet, ExpenseViewSet, ExpenseParticipantViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'balance', BalanceViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'expense-participants', ExpenseParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
