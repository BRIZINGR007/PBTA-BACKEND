from typing import Dict, cast

from ..repositories.expense_tracker import ExpenseTrackerRepository
from ..context import get_current_user
from ..services.expense_tracker import ExpenseTrackerService
from rest_framework.response import Response
from rest_framework import status


class ExpenseTracker:
    def __init__(self) -> None:
        self._expense_tracker_service = ExpenseTrackerService()
        self._expense_tracker_repo = ExpenseTrackerRepository()

    def add_transaction(self, transaction_data) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        self._expense_tracker_service.add_transaction(
            user_id=context_data.get("user_id"), transaction_data=transaction_data
        )
        return Response(
            {"message": "Transaction successfully added."},
            status=status.HTTP_201_CREATED,
        )

    def get_transactions(self, data) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        user_id = context_data.get("user_id")
        transactions = self._expense_tracker_repo.get_transactions(
            user_id, page=data["page"], month=data["month"]
        )
        return Response(transactions, status=status.HTTP_200_OK)

    def add_monthly_budget(self, budget_data) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        user_id = context_data.get("user_id")
        self._expense_tracker_repo.add_monthly_budget(
            user_id=user_id,
            month=budget_data["month"],
            amount=budget_data["amount"],
        )
        return Response(
            {"message": "Succesfully updated the monthly  budget."},
            status=status.HTTP_201_CREATED,
        )
