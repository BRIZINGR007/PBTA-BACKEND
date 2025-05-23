from decimal import Decimal
from django.db import transaction
from ..repositories.expense_tracker import ExpenseTrackerRepository


class ExpenseTrackerService:
    def __init__(self) -> None:
        self._expense_tracker_repo = ExpenseTrackerRepository()

    def add_transaction(self, user_id, transaction_data):
        amount = Decimal(transaction_data["amount"])
        transaction_type = transaction_data["transaction_type"]
        transaction_date = transaction_data["month"]

        with transaction.atomic():
            transaction_record = self._expense_tracker_repo.add_transaction(
                user_id, transaction_data
            )
            self._expense_tracker_repo.update_transaction_summary_by_month(
                user_id=user_id,
                transaction_type=transaction_type,
                amount=amount,
                transaction_date=transaction_date,
            )

        return transaction_record

    def edit_transaction(self, user_id, transaction_id, transaction_data):
        with transaction.atomic():
            self._expense_tracker_repo.edit_transaction(
                transaction_id=transaction_id, data=transaction_data
            )
            self._expense_tracker_repo.update_transaction_summary_by_month(
                user_id=user_id,
                transaction_type=transaction_data["transaction_type"],
                amount=transaction_data["amount"],
                transaction_date=transaction_data["month"],
            )
