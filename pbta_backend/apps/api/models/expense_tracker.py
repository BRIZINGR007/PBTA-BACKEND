from decimal import Decimal
import uuid
from django.db import models

from ..enums.enums import TransactionTypeEnums

from .user import User


class FinancialSummaryPerMonth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()  # use first day of the month
    total_expense = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    total_income = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    monthly_budget = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    class Meta:

        unique_together = ("user", "month")


class Transactions(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=30, choices=[(tag.value, tag.value) for tag in TransactionTypeEnums]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date}"
