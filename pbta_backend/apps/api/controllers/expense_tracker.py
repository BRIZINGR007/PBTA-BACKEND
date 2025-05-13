from typing import Dict, cast
from ..context import get_current_user
from ..services.expense_tracker import ExpenseTrackerService
from rest_framework.response import Response
from rest_framework import status


class ExpenseTracker:
    def __init__(self) -> None:
        self._expense_tracker_service = ExpenseTrackerService()

    def add_transaction(self, transaction_data) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        self._expense_tracker_service.add_transaction(
            user_id=context_data.get("user_id"), transaction_data=transaction_data
        )
        return Response(
            {"message": "Transaction successfully added."},
            status=status.HTTP_201_CREATED,
        )
    
