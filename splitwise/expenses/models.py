from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from decimal import Decimal


class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='expenses_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='expenses_users_permissions',
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ID: {self.pk}"

class Balance(models.Model):
    lender = models.ForeignKey(User, related_name='lent_balances', on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, related_name='borrowed_balances', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.borrower.username} owes {self.lender.username}: {self.amount}"

class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'

    SPLIT_CHOICES = [
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percent'),
    ]

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES)
    created_by = models.ForeignKey(User, related_name='created_expenses', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, through='ExpenseParticipant')

    def calculate_split(self):
        participants = self.participants.exclude(id=self.created_by.id)  # Exclude the creator

        if not participants.exists():
            raise ValueError("No participants to split the expense with.")

        if self.split_type == self.EQUAL:
            share = self.amount / participants.count()
            for participant in participants:
                self._update_balance(self.created_by, participant, share)

        elif self.split_type == self.EXACT:
            for participant in self.expenseparticipant_set.all():
                if participant.user != self.created_by:
                    self._update_balance(self.created_by, participant.user, participant.exact_amount)

        elif self.split_type == self.PERCENT:
            for participant in self.expenseparticipant_set.all():
                if participant.user != self.created_by:
                    amount_owed = (participant.percent / 100) * self.amount
                    self._update_balance(self.created_by, participant.user, amount_owed)

    def _update_balance(self, lender, borrower, amount):
        balance, created = Balance.objects.get_or_create(
            lender=lender,
            borrower=borrower,
            defaults={'amount': amount},
        )
        if not created:
            balance.amount += amount
            balance.save()

    def __str__(self):
        return f"{self.description} - {self.amount}"


class ExpenseParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exact_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user} owes {self.amount_owed} for {self.expense}"