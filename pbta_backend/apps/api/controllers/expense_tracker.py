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

    def add_transaction_summary_by_month(self, data) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        user_id = context_data.get("user_id")
        month_date = data["month"]
        self._expense_tracker_repo.add_transaction_summary_by_user_and_month(
            user_id=user_id, month=month_date
        )
        return Response(
            {"message": "Succesfully Added Transaction ."},
            status=status.HTTP_201_CREATED,
        )

    def get_transaction_summary_by_month(self, data) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        user_id = context_data.get("user_id")
        month_date = data["month"]
        transaction_summary = (
            self._expense_tracker_repo.get_transaction_summary_by_user_and_month(
                user_id=user_id, month=month_date
            )
        )
        return Response(
            transaction_summary,
            status=status.HTTP_201_CREATED,
        )

    def edit_transaction(self, transaction_id, data) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        user_id = context_data.get("user_id")
        self._expense_tracker_service.edit_transaction(user_id, transaction_id, data)
        return Response(
            {"message": "Succesfully  edited  transaction."},
            status=status.HTTP_201_CREATED,
        )

    def delete_transaction(self, transaction_id) -> Response:
        context_data = cast(Dict[str, str], get_current_user())
        user_id = context_data.get("user_id")
        self._expense_tracker_repo.delete_transaction(user_id, transaction_id)
        return Response(
            {"message": "Succesfully deleted transaction."},
            status=status.HTTP_200_OK,
        )
