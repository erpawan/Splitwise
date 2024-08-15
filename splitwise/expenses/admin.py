from django.contrib import admin

# Register your models here.
from .models import User, Expense, ExpenseParticipant

admin.site.register(User)
admin.site.register(Expense)
admin.site.register(ExpenseParticipant)