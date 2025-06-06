from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..controllers.expense_tracker import ExpenseTracker
from ..serializers.expense_tracker import (
    AddTransactionSummaryByMonthSerializer,
    EditTransactionSerializer,
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


@api_view(["POST"])
def add_transaction_summary_by_month(request):
    query_serializer = AddTransactionSummaryByMonthSerializer(data=request.query_params)
    query_serializer.is_valid(raise_exception=True)
    validated_data = query_serializer.validated_data
    return ExpenseTracker().add_transaction_summary_by_month(validated_data)


@api_view(["GET"])
def get_transaction_summary_by_month(request):
    query_serializer = AddTransactionSummaryByMonthSerializer(data=request.query_params)
    query_serializer.is_valid(raise_exception=True)
    validated_data = query_serializer.validated_data
    return ExpenseTracker().get_transaction_summary_by_month(validated_data)


@api_view(["PATCH"])
def edit_transaction(request):
    transaction_id = request.query_params.get("transaction_id")
    if not transaction_id:
        return Response(
            {"error": "transaction_id is required in query parameters."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = EditTransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    return ExpenseTracker().edit_transaction(
        transaction_id=transaction_id, data=validated_data
    )


@api_view(["DELETE"])
def delete_transaction(request):
    transaction_id = request.query_params.get("transaction_id")
    if not transaction_id:
        return Response(
            {"error": "transaction_id is required in query parameters."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return ExpenseTracker().delete_transaction(transaction_id)
