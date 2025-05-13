from rest_framework.decorators import api_view

from ..controllers.expense_tracker import ExpenseTracker
from ..serializers.expense_tracker import TransactionInputSerializer


@api_view(["POST"])
def add_transaction(request):
    serializer = TransactionInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    transaction_data = serializer.validated_data
    return ExpenseTracker().add_transaction(transaction_data)
