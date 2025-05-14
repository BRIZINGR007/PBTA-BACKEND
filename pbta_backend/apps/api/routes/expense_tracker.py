from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..controllers.expense_tracker import ExpenseTracker
from ..serializers.expense_tracker import (
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
    page = request.query_params.get("page", 1)
    try:
        page = int(page)
        if page < 1:
            raise ValueError("Page number must be 1 or higher.")
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return ExpenseTracker().get_transactions(page=page)


@api_view(["PATCH"])
def add_monthly_budget(request):
    serializer = MonthlyBudgetInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    monthly_budget_data = serializer.validated_data
    return ExpenseTracker().add_monthly_budget(budget_data=monthly_budget_data)
