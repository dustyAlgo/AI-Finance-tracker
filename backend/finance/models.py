from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
        # ML: suggested category (non-authoritative)
    predicted_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='predicted_transactions'
    )

    # ML: anomaly score (Z-score)
    anomaly_z_score = models.FloatField(
        null=True,
        blank=True
    )


    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )

    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    date = models.DateField()

    note = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

class MonthlySummary(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='monthly_summaries'
    )

    year = models.IntegerField()
    month = models.IntegerField()  # 1–12

    total_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_expense = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    savings = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'year', 'month')
