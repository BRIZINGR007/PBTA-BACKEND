from ..services.expense_tracker import ExpenseTrackerService
from rest_framework.response import Response


class ExpenseTracker:
    def __init__(self) -> None:
        self._expense_tracker_service = ExpenseTrackerService()

    def add_transaction(self, transaction_data) -> Response:
        pass
