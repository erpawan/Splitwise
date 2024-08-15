from rest_framework import viewsets
from .models import User, Balance, Expense, ExpenseParticipant
from .serializers import UserSerializer, BalanceSerializer, ExpenseSerializer, ExpenseParticipantSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

class ExpenseParticipantViewSet(viewsets.ModelViewSet):
    queryset = ExpenseParticipant.objects.all()
    serializer_class = ExpenseParticipantSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

