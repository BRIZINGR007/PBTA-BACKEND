from rest_framework import serializers
from ..models.expense_tracker import TransactionSummaryPerMonth, Transactions
from ..enums.enums import TransactionTypeEnums


class TransactionInputSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(
        choices=[(tag.value, tag.value) for tag in TransactionTypeEnums]
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
    month = serializers.DateField()

    class Meta:
        model = Transactions
        fields = ["transaction_type", "amount", "description", "month"]


class MonthlyBudgetInputSerializer(serializers.ModelSerializer):
    month = serializers.DateField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = TransactionSummaryPerMonth
        fields = ["month", "amount"]


class GetTransactionsQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1, default=1)
    month = serializers.DateField()


class AddTransactionSummaryByMonthSerializer(serializers.ModelSerializer):
    month = serializers.DateField()

    class Meta:
        model = TransactionSummaryPerMonth
        fields = ["month"]


class ResponseTransactionSummaryPerMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionSummaryPerMonth
        fields = "__all__"  # or specify fields manually


class ResponseTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"
