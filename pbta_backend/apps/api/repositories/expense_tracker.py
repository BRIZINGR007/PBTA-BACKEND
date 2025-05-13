from decimal import Decimal
from datetime import date
from uuid import UUID
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from ..enums.enums import TransactionCategoryEnums, TransactionTypeEnums
from ..models.expense_tracker import Transactions, TransactionSummaryPerMonth


class ExpenseTrackerRepository:
    @staticmethod
    def add_transaction(user_id: str, data: dict):
        if data["transaction_type"] == TransactionTypeEnums.SALARY:
            transaction_category = TransactionCategoryEnums.INCOME.value
        else:
            transaction_category = TransactionCategoryEnums.EXPENSES.value

        return Transactions.objects.create(
            user_id=user_id,
            transaction_type=data["transaction_type"],
            transaction_category=transaction_category,
            amount=Decimal(data["amount"]),
            description=data.get("description", ""),
            date=data["date"],
        )

    @staticmethod
    def update_transaction_summary_by_month(
        user_id: str, transaction_type: str, amount: Decimal, transaction_date: date
    ):
        month_start = transaction_date.replace(day=1)

        summary, _ = TransactionSummaryPerMonth.objects.get_or_create(
            user_id=UUID(user_id),
            month=month_start,
            defaults={
                "total_expense": Decimal("0.00"),
                "total_income": Decimal("0.00"),
                "balance": Decimal("0.00"),
                "monthly_budget": Decimal("0.00"),
            },
        )

        if transaction_type == TransactionTypeEnums.SALARY:
            summary.total_income += amount
        else:
            summary.total_expense += amount

        summary.balance = summary.total_income - summary.total_expense
        summary.save()

        return summary

    @staticmethod
    def get_transactions(user_id, page=1, page_size=10):
        transactions = Transactions.objects.filter(user_id=user_id).order_by("-date")

        paginator = Paginator(transactions, page_size)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        transactions_serialized = [
            model_to_dict(
                t,
                fields=[
                    "id",
                    "transaction_type",
                    "transaction_category",
                    "amount",
                    "description",
                    "date",
                ],
            )
            for t in transactions_page.object_list
        ]

        return {
            "transactions": transactions_serialized,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": transactions_page.number,
        }
