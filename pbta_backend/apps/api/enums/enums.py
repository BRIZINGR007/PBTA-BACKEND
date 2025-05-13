from enum import StrEnum


class TransactionTypeEnums(StrEnum):
    SALARY = "Salary"
    GROCERY = "Grocery"
    ENTERTAINMENT = "Entertainment"
    FASHION = "Fashion"


class TransactionCategoryEnums(StrEnum):
    INCOME = "Income"
    EXPENSES = "Expenses"
