from ..models.expense_tracker import Transactions


class ExpenseTrackerRepository:
    @staticmethod
    def add_transaction(data):
        return Transactions.objects.create(**data)
    
