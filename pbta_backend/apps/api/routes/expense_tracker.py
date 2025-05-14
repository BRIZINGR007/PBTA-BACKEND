from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..controllers.expense_tracker import ExpenseTracker
from ..serializers.expense_tracker import (
    GetTransactionsQuerySerializer,
    MonthlyBudgetInputSerializer,
    TransactionInputSerializer,
)


@api_view(["POST"])
def add_transaction(request):
    serializer = TransactionInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    transaction_data = serializer.validated_data
    return ExpenseTracker().add_transaction(transaction_data)


@api_view(["GET"])
def get_transactions(request):
    query_serializer = GetTransactionsQuerySerializer(data=request.query_params)
    query_serializer.is_valid(raise_exception=True)
    validated_data = query_serializer.validated_data
    return ExpenseTracker().get_transactions(data=validated_data)


@api_view(["PATCH"])
def add_monthly_budget(request):
    serializer = MonthlyBudgetInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    monthly_budget_data = serializer.validated_data
    return ExpenseTracker().add_monthly_budget(budget_data=monthly_budget_data)
