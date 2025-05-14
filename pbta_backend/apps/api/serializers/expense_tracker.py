from rest_framework import serializers
from ..models.expense_tracker import TransactionSummaryPerMonth, Transactions
from ..enums.enums import TransactionTypeEnums


class TransactionInputSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(
        choices=[(tag.value, tag.value) for tag in TransactionTypeEnums]
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField()

    class Meta:
        model = Transactions
        fields = ["transaction_type", "amount", "description", "date"]


class MonthlyBudgetInputSerializer(serializers.ModelSerializer):
    month = serializers.DateField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = TransactionSummaryPerMonth
        fields = ["month", "amount"]
