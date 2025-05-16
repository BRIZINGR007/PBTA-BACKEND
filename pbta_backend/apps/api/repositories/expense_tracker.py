from decimal import Decimal
from datetime import date
from uuid import UUID
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..serializers.expense_tracker import (
    ResponseTransactionSummaryPerMonthSerializer,
    ResponseTransactionsSerializer,
)
from ..enums.enums import TransactionCategoryEnums, TransactionTypeEnums
from ..models.expense_tracker import Transactions, TransactionSummaryPerMonth


class ExpenseTrackerRepository:
    @staticmethod
    def add_transaction(user_id: str, data: dict):
        if data["transaction_type"] == TransactionTypeEnums.SALARY:
            transaction_category = TransactionCategoryEnums.INCOME.value
        else:
            transaction_category = TransactionCategoryEnums.EXPENSES.value
        month_start = data["month"].replace(day=1)
        return Transactions.objects.create(
            user_id=user_id,
            transaction_type=data["transaction_type"],
            transaction_category=transaction_category,
            amount=Decimal(data["amount"]),
            description=data.get("description", ""),
            month=month_start,
        )

    @staticmethod
    def add_transaction_summary_by_user_and_month(user_id, month: date):
        month_start = month.replace(day=1)
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
        summary.save()

    @staticmethod
    def get_transaction_summary_by_user_and_month(user_id, month: date):
        month_start = month.replace(day=1)
        summary, created = TransactionSummaryPerMonth.objects.get_or_create(
            user_id=UUID(user_id),
            month=month_start,
            defaults={
                "total_expense": Decimal("0.00"),
                "total_income": Decimal("0.00"),
                "balance": Decimal("0.00"),
                "monthly_budget": Decimal("0.00"),
            },
        )

        if created:
            summary.save()

        # Return the serialized data
        return ResponseTransactionSummaryPerMonthSerializer(summary).data

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
    def get_transactions(user_id, month, page=1, page_size=10):
        month_start = month.replace(day=1)

        transactions = Transactions.objects.filter(
            user_id=user_id, month=month_start
        ).order_by("-created_at")

        paginator = Paginator(transactions, page_size)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        transactions_serialized = [
            ResponseTransactionsSerializer(t).data
            for t in transactions_page.object_list
        ]

        return {
            "transactions": transactions_serialized,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": transactions_page.number,
        }

    @staticmethod
    def add_monthly_budget(user_id, month, amount):
        month_start = month.replace(day=1)
        summary, created = TransactionSummaryPerMonth.objects.get_or_create(
            user_id=user_id,
            month=month_start,
            defaults={"monthly_budget": amount},
        )

        if not created:
            summary.monthly_budget = amount
            summary.save()

        return summary

    @staticmethod
    def edit_transaction(transaction_id, data):
        transaction = Transactions.objects.get(transaction_id=UUID(transaction_id))
        if "transaction_type" in data:
            if data["transaction_type"] == TransactionTypeEnums.SALARY:
                data["transaction_category"] = TransactionCategoryEnums.INCOME.value
            else:
                data["transaction_category"] = TransactionCategoryEnums.EXPENSES.value

        for field, value in data.items():
            setattr(transaction, field, value)
        transaction.save()

    @staticmethod
    def delete_transaction(user_id, transaction_id):
        with transaction.atomic():
            # Fetch the transaction
            transaction_obj = Transactions.objects.get(
                transaction_id=UUID(transaction_id)
            )

            # Extract necessary details before deleting
            transaction_type = transaction_obj.transaction_type
            amount = transaction_obj.amount
            transaction_date = transaction_obj.month

            # Delete the transaction
            transaction_obj.delete()

            # Update the summary to subtract the deleted transaction
            month_start = transaction_date.replace(day=1)

            summary = TransactionSummaryPerMonth.objects.get(
                user_id=UUID(user_id),
                month=month_start,
            )

            if transaction_type == TransactionTypeEnums.SALARY:
                summary.total_income -= amount
            else:
                summary.total_expense -= amount

            summary.balance = summary.total_income - summary.total_expense
            summary.save()
