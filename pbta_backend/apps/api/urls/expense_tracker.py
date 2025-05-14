from django.urls import path

from ..routes import expense_tracker

expense_tracker_urls = [
    path("add-transaction/", expense_tracker.add_transaction),
    path("get-transactions/", expense_tracker.get_transactions),
    path("add-monthly-budget/", expense_tracker.add_monthly_budget),
    path(
        "add-transaction-summary-by-month/",
        expense_tracker.add_transaction_summary_by_month,
    ),
    path(
        "get-transaction-summary-by-month/",
        expense_tracker.get_transaction_summary_by_month,
    ),
]
