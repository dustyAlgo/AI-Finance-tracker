from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'

    class Category(models.TextChoices):
        FOOD = 'FOOD', 'Food'
        RENT = 'RENT', 'Rent'
        TRAVEL = 'TRAVEL', 'Travel'
        FITNESS = 'FITNESS', 'Fitness'
        MEDICAL = 'MEDICAL', 'Medical'
        SALARY = 'SALARY', 'Salary'
        OTHERS = 'OTHERS', 'Others'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    amount = models.DecimalField(
        max_digits=8,       # up to 999,999.99 (safe for < 3 lakh)
        decimal_places=2
    )

    date = models.DateField()

    note = models.CharField(
        max_length=255,
        blank=True
    )
    class Meta:
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'type']),
            models.Index(fields=['user', 'category']),
        ]


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | {self.type} | {self.amount}"
