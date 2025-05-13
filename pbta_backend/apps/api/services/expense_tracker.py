from decimal import Decimal
from django.db import transaction
from ..repositories.expense_tracker import ExpenseTrackerRepository


class ExpenseTrackerService:
    def __init__(self) -> None:
        self._expense_tracker_repo = ExpenseTrackerRepository()

    def get_all_transactions(self, user_id):
        pass

    def add_transaction(self, user_id, transaction_data):
        amount = Decimal(transaction_data["amount"])
        transaction_type = transaction_data["transaction_type"]
        transaction_date = transaction_data["date"]

        with transaction.atomic():
            # Create transaction
            transaction_record = self._expense_tracker_repo.add_transaction(
                user_id, transaction_data
            )

            # Update monthly summary
            self._expense_tracker_repo.update_transaction_summary_by_month(
                user_id=user_id,
                transaction_type=transaction_type,
                amount=amount,
                transaction_date=transaction_date,
            )

        return transaction_record
