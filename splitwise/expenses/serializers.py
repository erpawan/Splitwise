from rest_framework import serializers
from .models import User, Balance, Expense, ExpenseParticipant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['lender', 'borrower', 'amount']


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ExpenseParticipant
        fields = ['user', 'exact_amount', 'percent']


class ExpenseSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    participants = ExpenseParticipantSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'split_type', 'created_by', 'participants']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        expense = Expense.objects.create(**validated_data)
        for participant_data in participants_data:
            ExpenseParticipant.objects.create(expense=expense, **participant_data)
        return expense

    def update(self, instance, validated_data):
        participants_data = validated_data.pop('participants')
        instance.description = validated_data.get('description', instance.description)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.split_type = validated_data.get('split_type', instance.split_type)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()

        # Update participants
        for participant_data in participants_data:
            user_id = participant_data.get('user')
            amount_owed = participant_data.get('amount_owed', 0)
            exact_amount = participant_data.get('exact_amount')
            percent = participant_data.get('percent')
            ExpenseParticipant.objects.update_or_create(
                expense=instance,
                user=user_id,
                defaults={'amount_owed': amount_owed, 'exact_amount': exact_amount, 'percent': percent}
            )
        return instance
