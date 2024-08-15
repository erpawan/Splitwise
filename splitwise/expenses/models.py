from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='expenses_users',  # Change related_name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='expenses_users_permissions',  # Change related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


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

    def __str__(self):
        return f"{self.description} - {self.amount}"


class ExpenseParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user} owes {self.amount_owed} for {self.expense}"
